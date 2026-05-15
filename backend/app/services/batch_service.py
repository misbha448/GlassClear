from __future__ import annotations

import json
import mimetypes
import os
import shutil
import threading
import uuid
import zipfile
from datetime import datetime
from pathlib import Path

import cv2
from fastapi import BackgroundTasks, HTTPException, UploadFile
from PIL import Image
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.batch_job import BatchJob, BatchJobItem
from app.models.prediction import Prediction
from app.models.user import User
from app.services.dashboard_service import assign_prediction_category, file_path_to_url
from app.services.editor_service import create_edit_version
from app.services.inference_service import run_reflection_removal
from app.services.prediction_service import create_prediction
from app.utils.export_utils import save_image_for_export

MAX_BATCH_FILES = 20
MAX_IMAGE_SIZE = 5 * 1024 * 1024
MAX_WORKING_DIMENSION = 1280
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
_BATCH_PROCESSING_LOCK = threading.Lock()


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _uploads_root() -> Path:
    return (_project_root() / "uploads").resolve()


def _ensure_upload_dirs() -> None:
    for relative in ("original", "output", "thumbnails", "batch_working", "batch_zips"):
        (_uploads_root() / relative).mkdir(parents=True, exist_ok=True)


def _file_size(upload: UploadFile) -> int:
    current_position = upload.file.tell()
    upload.file.seek(0, os.SEEK_END)
    size = upload.file.tell()
    upload.file.seek(current_position)
    return size


def _validate_upload(file: UploadFile) -> None:
    extension = Path(file.filename or "").suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid file type")

    size = _file_size(file)
    if size > MAX_IMAGE_SIZE:
        raise HTTPException(status_code=400, detail=f"File too large: {file.filename}")


def _save_upload_file(file: UploadFile) -> tuple[str, dict]:
    _ensure_upload_dirs()
    extension = Path(file.filename or "").suffix.lower()
    stored_name = f"batch_{uuid.uuid4().hex}{extension}"
    original_path = _uploads_root() / "original" / stored_name

    file.file.seek(0)
    with open(original_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    with Image.open(original_path) as image:
        width, height = image.size
        thumbnail = image.copy()
        thumbnail.thumbnail((320, 240))
        thumbnail_path = _uploads_root() / "thumbnails" / f"thumb_{Path(stored_name).stem}.jpg"
        thumbnail.convert("RGB").save(thumbnail_path, "JPEG", quality=90)

    return str(original_path), {
        "stored_name": stored_name,
        "file_size": os.path.getsize(original_path),
        "mime_type": file.content_type or mimetypes.guess_type(file.filename or "")[0] or "image/jpeg",
        "width": width,
        "height": height,
        "thumbnail_path": str(thumbnail_path),
    }


def _serialize_batch_item(item: BatchJobItem, prediction: Prediction) -> dict:
    return {
        "id": item.id,
        "image_id": prediction.id,
        "filename": prediction.original_filename or os.path.basename(prediction.original_image_path),
        "status": item.status,
        "original_url": file_path_to_url(prediction.original_image_path),
        "processed_url": file_path_to_url(prediction.output_image_path),
        "error_message": item.error_message,
        "created_at": item.created_at.isoformat() if item.created_at else None,
    }


def upload_batch(
    db: Session,
    user: User,
    files: list[UploadFile],
    project_id: int | None = None,
    tool: str = "remove_reflection",
    settings_json: str | None = None,
) -> dict:
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded")
    if len(files) > MAX_BATCH_FILES:
        raise HTTPException(status_code=400, detail="Too many files. Maximum 20 images allowed.")
    if tool != "remove_reflection":
        raise HTTPException(status_code=400, detail="Only reflection removal is supported for batch processing.")

    try:
        settings = json.loads(settings_json) if settings_json else {}
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=400, detail="Invalid batch settings") from exc

    for file in files:
        _validate_upload(file)

    batch = BatchJob(
        user_id=user.id,
        project_id=project_id,
        name=f"Batch {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}",
        status="queued",
        total_count=len(files),
        completed_count=0,
        failed_count=0,
        settings={"tool": tool, "settings": settings},
    )
    db.add(batch)
    db.commit()
    db.refresh(batch)

    items = []
    for file in files:
        original_path, metadata = _save_upload_file(file)
        prediction = create_prediction(
            db=db,
            user_id=user.id,
            original_image_path=original_path,
            output_image_path=None,
            status_value="queued",
            model_name="RDNet",
            mode="clean",
            image_size=f"{metadata['file_size'] / (1024 * 1024):.2f} MB",
            processing_time=None,
            project_id=project_id,
            original_filename=file.filename,
            stored_filename=metadata["stored_name"],
            mime_type=metadata["mime_type"],
            file_size=metadata["file_size"],
            width=metadata["width"],
            height=metadata["height"],
            source="batch",
            active_workspace=False,
            thumbnail_path=metadata["thumbnail_path"],
        )

        item = BatchJobItem(batch_job_id=batch.id, image_id=prediction.id, status="queued")
        db.add(item)
        db.commit()
        db.refresh(item)
        items.append(_serialize_batch_item(item, prediction))

    return {"batch_id": batch.id, "status": batch.status, "total_count": batch.total_count, "items": items}


def _prepare_working_copy(original_path: str, item_id: int) -> str:
    _ensure_upload_dirs()
    working_extension = Path(original_path).suffix.lower() or ".jpg"
    working_path = _uploads_root() / "batch_working" / f"working_{item_id}_{uuid.uuid4().hex}{working_extension}"

    with Image.open(original_path) as image:
        image = image.convert("RGB")
        max_dimension = max(image.size)
        if max_dimension > MAX_WORKING_DIMENSION:
            scale = MAX_WORKING_DIMENSION / float(max_dimension)
            resized = (
                max(1, int(image.width * scale)),
                max(1, int(image.height * scale)),
            )
            image = image.resize(resized, Image.Resampling.LANCZOS)
        image.save(working_path)

    return str(working_path)


def _build_batch_zip(batch: BatchJob, db: Session) -> str | None:
    completed_items = (
        db.query(BatchJobItem, Prediction)
        .join(Prediction, Prediction.id == BatchJobItem.image_id)
        .filter(BatchJobItem.batch_job_id == batch.id, BatchJobItem.status == "completed", Prediction.output_image_path.isnot(None))
        .all()
    )
    if not completed_items:
        return None

    _ensure_upload_dirs()
    zip_path = _uploads_root() / "batch_zips" / f"batch_{batch.id}_{uuid.uuid4().hex}.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for _, prediction in completed_items:
            if prediction.output_image_path and os.path.exists(prediction.output_image_path):
                archive.write(
                    prediction.output_image_path,
                    arcname=os.path.basename(prediction.output_image_path),
                )
    return str(zip_path)


def _process_batch_job(batch_id: int, user_id: int) -> None:
    db = SessionLocal()
    try:
        with _BATCH_PROCESSING_LOCK:
            batch = db.query(BatchJob).filter(BatchJob.id == batch_id, BatchJob.user_id == user_id).first()
            if not batch:
                return

            batch.status = "processing"
            batch.completed_count = 0
            batch.failed_count = 0
            batch.zip_path = None
            db.commit()

            items = (
                db.query(BatchJobItem)
                .filter(BatchJobItem.batch_job_id == batch.id)
                .order_by(BatchJobItem.created_at.asc(), BatchJobItem.id.asc())
                .all()
            )

            for item in items:
                prediction = db.query(Prediction).filter(Prediction.id == item.image_id, Prediction.user_id == user_id).first()
                if not prediction:
                    item.status = "failed"
                    item.error_message = "Image not found"
                    batch.failed_count += 1
                    db.commit()
                    continue

                item.status = "processing"
                item.error_message = None
                prediction.status = "processing"
                db.commit()

                working_copy = None
                try:
                    working_copy = _prepare_working_copy(prediction.original_image_path, item.id)
                    results = run_reflection_removal(working_copy, str(_uploads_root()), uuid.uuid4().hex)
                    final_extension = Path(prediction.original_filename or prediction.original_image_path).suffix.lower() or ".jpg"
                    export_path = _uploads_root() / "output" / f"batch_clean_{uuid.uuid4().hex}{final_extension}"
                    processed_image = cv2.imread(results["final"], cv2.IMREAD_COLOR)
                    final_output_path = save_image_for_export(processed_image, str(export_path))

                    prediction.output_image_path = final_output_path
                    prediction.status = "completed"
                    prediction.processing_time = results["time"]
                    prediction.updated_at = datetime.utcnow()
                    assign_prediction_category(db, prediction)

                    create_edit_version(
                        db,
                        user_id=user_id,
                        image_id=prediction.id,
                        project_id=prediction.project_id,
                        version_name="Batch Restore",
                        version_type="processed",
                        file_path=final_output_path,
                        settings={"batch_id": batch.id},
                        ml_metadata={
                            "confidence": round(results["metrics"]["ssim"] * 100, 2),
                            "reflection_removed": round(results["metrics"]["edge_score"] * 100, 2),
                            "processing_time": results["time"],
                        },
                        is_active=False,
                    )

                    item.status = "completed"
                    batch.completed_count += 1
                except Exception as exc:
                    prediction.status = "failed"
                    prediction.updated_at = datetime.utcnow()
                    item.status = "failed"
                    item.error_message = str(exc)
                    batch.failed_count += 1
                finally:
                    if working_copy and os.path.exists(working_copy):
                        try:
                            os.remove(working_copy)
                        except OSError:
                            pass
                    db.commit()

            if batch.completed_count and batch.failed_count:
                batch.status = "partially_failed"
            elif batch.completed_count == batch.total_count:
                batch.status = "completed"
            elif batch.failed_count == batch.total_count:
                batch.status = "failed"
            else:
                batch.status = "completed"

            zip_path = _build_batch_zip(batch, db)
            batch.zip_path = zip_path
            db.commit()
    finally:
        db.close()


def start_batch(db: Session, user: User, batch_id: int, background_tasks: BackgroundTasks | None = None) -> dict:
    batch = db.query(BatchJob).filter(BatchJob.id == batch_id, BatchJob.user_id == user.id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")

    if batch.status == "processing":
        return {"batch_id": batch.id, "status": batch.status, "message": "Batch processing started."}

    items_count = db.query(BatchJobItem).filter(BatchJobItem.batch_job_id == batch.id).count()
    if items_count == 0:
        raise HTTPException(status_code=400, detail="Batch has no items")

    batch.status = "processing"
    batch.completed_count = 0
    batch.failed_count = 0
    batch.zip_path = None
    db.commit()

    if background_tasks is not None:
        background_tasks.add_task(_process_batch_job, batch.id, user.id)
    else:
        _process_batch_job(batch.id, user.id)

    return {"success": True, "batch_id": batch.id, "status": "processing", "message": "Batch processing started."}


def get_batch(db: Session, user: User, batch_id: int) -> dict:
    batch = db.query(BatchJob).filter(BatchJob.id == batch_id, BatchJob.user_id == user.id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")

    rows = (
        db.query(BatchJobItem, Prediction)
        .join(Prediction, Prediction.id == BatchJobItem.image_id)
        .filter(BatchJobItem.batch_job_id == batch.id)
        .order_by(BatchJobItem.created_at.asc(), BatchJobItem.id.asc())
        .all()
    )
    return {
        "batch_id": batch.id,
        "status": batch.status,
        "total_count": batch.total_count,
        "completed_count": batch.completed_count,
        "failed_count": batch.failed_count,
        "items": [_serialize_batch_item(item, prediction) for item, prediction in rows],
        "zip_url": file_path_to_url(batch.zip_path),
    }


def list_batches(db: Session, user: User) -> dict:
    batches = db.query(BatchJob).filter(BatchJob.user_id == user.id).order_by(BatchJob.updated_at.desc()).all()
    return {
        "batches": [
            {
                "batch_id": batch.id,
                "status": batch.status,
                "total_count": batch.total_count,
                "completed_count": batch.completed_count,
                "failed_count": batch.failed_count,
                "zip_url": file_path_to_url(batch.zip_path),
            }
            for batch in batches
        ]
    }


def get_batch_zip_path(db: Session, user: User, batch_id: int) -> str:
    batch = db.query(BatchJob).filter(BatchJob.id == batch_id, BatchJob.user_id == user.id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    if batch.status not in {"completed", "partially_failed"}:
        raise HTTPException(status_code=400, detail="Batch is not completed yet.")
    if not batch.zip_path or not os.path.exists(batch.zip_path):
        raise HTTPException(status_code=404, detail="Batch zip not found")
    return batch.zip_path
