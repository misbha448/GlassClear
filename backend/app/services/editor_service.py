from __future__ import annotations

import json
import mimetypes
import os
import shutil
import uuid
from datetime import datetime
from pathlib import Path

from fastapi import HTTPException, UploadFile, status
from fastapi.responses import FileResponse
from PIL import Image, ImageDraw
from sqlalchemy.orm import Session

from app.models.edit_version import EditVersion
from app.models.prediction import Prediction
from app.models.user import User
from app.services.dashboard_service import file_path_to_url, get_demo_asset_paths, serialize_prediction
from app.services.inference_service import run_reflection_removal
from app.services.prediction_service import create_prediction, get_prediction_by_id, set_active_workspace_prediction
from app.utils.export_utils import save_image_for_export
from app.utils.filename_generator import normalize_extension

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def _ensure_upload_dirs() -> None:
    for directory in ("uploads", "uploads/original", "uploads/output", "uploads/exports", "uploads/thumbnails"):
        os.makedirs(directory, exist_ok=True)


def _validate_image_file(filename: str) -> None:
    extension = Path(filename).suffix.lower()
    if extension not in IMAGE_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid file type")


def _save_upload(file: UploadFile) -> tuple[str, dict]:
    _ensure_upload_dirs()
    _validate_image_file(file.filename)
    extension = Path(file.filename).suffix.lower()
    stored_name = f"upload_{uuid.uuid4().hex}{extension}"
    stored_path = os.path.join("uploads", "original", stored_name)

    with open(stored_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    with Image.open(stored_path) as image:
        width, height = image.size
        thumbnail = image.copy()
        thumbnail.thumbnail((320, 240))
        thumbnail_path = os.path.join("uploads", "thumbnails", f"thumb_{stored_name}.jpg")
        thumbnail.convert("RGB").save(thumbnail_path, "JPEG", quality=92)

    metadata = {
        "stored_name": stored_name,
        "mime_type": file.content_type or mimetypes.guess_type(file.filename)[0] or "image/jpeg",
        "file_size": os.path.getsize(stored_path),
        "width": width,
        "height": height,
        "thumbnail_path": thumbnail_path,
    }
    return stored_path, metadata


def _version_label_from_settings(settings: dict | None) -> str:
    if not settings:
        return "Processed Restore"
    strength = settings.get("strength", "balanced")
    if strength == "soft":
        return "Detail Preserve"
    if strength == "strong":
        return "Strong Clean"
    return "Balanced Restore"


def create_edit_version(
    db: Session,
    *,
    user_id: int,
    image_id: int,
    project_id: int | None,
    version_name: str,
    version_type: str,
    file_path: str,
    settings: dict | None = None,
    ml_metadata: dict | None = None,
    is_active: bool = False,
) -> EditVersion:
    if is_active:
        db.query(EditVersion).filter(EditVersion.user_id == user_id, EditVersion.image_id == image_id).update(
            {EditVersion.is_active: False},
            synchronize_session=False,
        )

    version = EditVersion(
        user_id=user_id,
        image_id=image_id,
        project_id=project_id,
        version_name=version_name,
        version_type=version_type,
        file_path=file_path,
        settings=settings,
        ml_metadata=ml_metadata,
        is_active=is_active,
    )
    db.add(version)
    db.commit()
    db.refresh(version)
    return version


def upload_editor_image(db: Session, user: User, file: UploadFile, project_id: int | None = None) -> dict:
    stored_path, metadata = _save_upload(file)
    prediction = create_prediction(
        db=db,
        user_id=user.id,
        original_image_path=stored_path,
        output_image_path=None,
        status_value="uploaded",
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
        source="dashboard",
        active_workspace=True,
        thumbnail_path=metadata["thumbnail_path"],
    )
    set_active_workspace_prediction(db, user.id, prediction.id)
    version = create_edit_version(
        db,
        user_id=user.id,
        image_id=prediction.id,
        project_id=project_id,
        version_name="Original Upload",
        version_type="original",
        file_path=stored_path,
        is_active=True,
    )
    return {"image": serialize_prediction(prediction), "version": serialize_version(version)}


def serialize_version(version: EditVersion) -> dict:
    return {
        "id": version.id,
        "image_id": version.image_id,
        "version_name": version.version_name,
        "version_type": version.version_type,
        "file_url": file_path_to_url(version.file_path),
        "settings": version.settings,
        "ml_metadata": version.ml_metadata,
        "is_active": version.is_active,
        "created_at": version.created_at.isoformat(),
    }


def get_current_image(db: Session, user: User) -> dict | None:
    prediction = (
        db.query(Prediction)
        .filter(Prediction.user_id == user.id)
        .order_by(Prediction.active_workspace.desc(), Prediction.updated_at.desc(), Prediction.created_at.desc())
        .first()
    )
    return serialize_prediction(prediction)


def set_current_image(db: Session, user: User, image_id: int) -> dict:
    prediction = set_active_workspace_prediction(db, user.id, image_id)
    return serialize_prediction(prediction)


def apply_tool(db: Session, user: User, image_id: int, tool: str, settings: dict | None) -> dict:
    prediction = get_prediction_by_id(db, image_id, user.id)
    settings = settings or {}
    if tool != "remove_reflection":
        raise HTTPException(status_code=501, detail=f"{tool} is not implemented yet")

    if not prediction.original_image_path or not os.path.exists(prediction.original_image_path):
        raise HTTPException(status_code=404, detail="Original image not found")

    unique_id = uuid.uuid4().hex
    results = run_reflection_removal(prediction.original_image_path, "uploads", unique_id)
    prediction.output_image_path = results["final"]
    prediction.status = "completed"
    prediction.processing_mode = settings.get("strength", "balanced")
    prediction.processing_time = results["time"]
    prediction.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(prediction)
    set_active_workspace_prediction(db, user.id, prediction.id)

    version = create_edit_version(
        db,
        user_id=user.id,
        image_id=prediction.id,
        project_id=prediction.project_id,
        version_name=_version_label_from_settings(settings),
        version_type="processed",
        file_path=results["final"],
        settings=settings,
        ml_metadata={
            "confidence": round(results["metrics"]["ssim"] * 100, 2),
            "reflection_removed": round(results["metrics"]["edge_score"] * 100, 2),
            "processing_time": results["time"],
        },
        is_active=True,
    )

    return {"success": True, "image": serialize_prediction(prediction), "version": serialize_version(version)}


def get_versions_for_image(db: Session, user: User, image_id: int) -> dict:
    get_prediction_by_id(db, image_id, user.id)
    versions = (
        db.query(EditVersion)
        .filter(EditVersion.user_id == user.id, EditVersion.image_id == image_id)
        .order_by(EditVersion.created_at.asc())
        .all()
    )
    return {"image_id": image_id, "versions": [serialize_version(version) for version in versions]}


def activate_version(db: Session, user: User, version_id: int) -> dict:
    version = db.query(EditVersion).filter(EditVersion.id == version_id, EditVersion.user_id == user.id).first()
    if not version:
        raise HTTPException(status_code=404, detail="Version not found")

    db.query(EditVersion).filter(EditVersion.user_id == user.id, EditVersion.image_id == version.image_id).update(
        {EditVersion.is_active: False},
        synchronize_session=False,
    )
    version.is_active = True
    prediction = get_prediction_by_id(db, version.image_id, user.id)
    if version.version_type == "processed":
        prediction.output_image_path = version.file_path
    set_active_workspace_prediction(db, user.id, prediction.id)
    db.commit()
    db.refresh(version)
    db.refresh(prediction)
    return {"image": serialize_prediction(prediction), "version": serialize_version(version)}


def get_recent_edits(db: Session, user: User) -> dict:
    versions = (
        db.query(EditVersion)
        .filter(EditVersion.user_id == user.id)
        .order_by(EditVersion.created_at.desc())
        .limit(12)
        .all()
    )
    return {"recent_edits": [serialize_version(version) for version in versions]}


def download_image(db: Session, user: User, image_id: int) -> FileResponse:
    prediction = get_prediction_by_id(db, image_id, user.id)
    path = prediction.output_image_path or prediction.original_image_path
    if not path or not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Image file not found")
    media_type = mimetypes.guess_type(path)[0] or "application/octet-stream"
    return FileResponse(path=path, media_type=media_type, filename=os.path.basename(path))


def _generate_before_after_export(prediction: Prediction, export_title: str) -> str:
    _ensure_upload_dirs()
    if not prediction.output_image_path or not os.path.exists(prediction.output_image_path):
        raise HTTPException(status_code=400, detail="Processed image unavailable for export")

    original = Image.open(prediction.original_image_path).convert("RGB")
    processed = Image.open(prediction.output_image_path).convert("RGB")
    width = max(original.width, processed.width)
    height = max(original.height, processed.height)
    original = original.resize((width, height))
    processed = processed.resize((width, height))
    canvas = Image.new("RGB", (width * 2, height + 90), "#f4f7fd")
    canvas.paste(original, (0, 90))
    canvas.paste(processed, (width, 90))
    draw = ImageDraw.Draw(canvas)
    draw.text((30, 28), f"{export_title} - BEFORE", fill="#18253c")
    draw.text((width + 30, 28), f"{export_title} - AFTER", fill="#18253c")
    output_path = os.path.join("uploads", "exports", f"compare_{uuid.uuid4().hex}.jpg")
    canvas.save(output_path, "JPEG", quality=95)
    return output_path


def export_image(db: Session, user: User, image_id: int, export_type: str) -> dict:
    prediction = get_prediction_by_id(db, image_id, user.id)
    export_type = export_type or "processed"

    if export_type == "processed":
        return {"status": "ready", "download_url": file_path_to_url(prediction.output_image_path or prediction.original_image_path)}

    if export_type == "hd_final_render":
        return {"status": "ready", "download_url": file_path_to_url(prediction.output_image_path or prediction.original_image_path)}

    if export_type in {"before_after_comparison", "client_presentation"}:
        output_path = _generate_before_after_export(prediction, "GlassClear")
        return {"status": "generated", "download_url": file_path_to_url(output_path)}

    if export_type == "architect_report_pack":
        return {
            "status": "not_supported",
            "report": {
                "image_id": prediction.id,
                "filename": prediction.original_filename,
                "processing_mode": prediction.processing_mode,
                "processing_time": prediction.processing_time,
            },
        }

    raise HTTPException(status_code=400, detail="Unsupported export type")


def claim_guest_image(db: Session, user: User, guest_image_token: str) -> dict:
    prediction = (
        db.query(Prediction)
        .filter(Prediction.guest_image_token == guest_image_token, Prediction.user_id.is_(None))
        .first()
    )
    if not prediction:
        raise HTTPException(status_code=404, detail="Guest image not found")

    prediction.user_id = user.id
    prediction.source = "guest"
    prediction.active_workspace = True
    db.commit()
    db.refresh(prediction)
    set_active_workspace_prediction(db, user.id, prediction.id)

    original_exists = (
        db.query(EditVersion)
        .filter(EditVersion.image_id == prediction.id, EditVersion.version_type == "original")
        .first()
    )
    if not original_exists:
        create_edit_version(
            db,
            user_id=user.id,
            image_id=prediction.id,
            project_id=prediction.project_id,
            version_name="Original Upload",
            version_type="original",
            file_path=prediction.original_image_path,
            is_active=not prediction.output_image_path,
        )

    if prediction.output_image_path:
        processed_exists = (
            db.query(EditVersion)
            .filter(EditVersion.image_id == prediction.id, EditVersion.version_type == "processed")
            .first()
        )
        if not processed_exists:
            create_edit_version(
                db,
                user_id=user.id,
                image_id=prediction.id,
                project_id=prediction.project_id,
                version_name="Balanced Restore",
                version_type="processed",
                file_path=prediction.output_image_path,
                is_active=True,
            )

    from app.services.dashboard_service import build_workspace_payload

    return build_workspace_payload(db, user)


def get_demo_image_payload() -> dict:
    original_path, processed_path = get_demo_asset_paths()
    return {
        "original_url": file_path_to_url(original_path),
        "processed_url": file_path_to_url(processed_path),
        "filename": "Sample Architectural Image",
    }


def use_demo_image(db: Session, user: User) -> dict:
    original_path, processed_path = get_demo_asset_paths()
    with Image.open(original_path) as demo_image:
        width, height = demo_image.size
    prediction = create_prediction(
        db=db,
        user_id=user.id,
        original_image_path=original_path,
        output_image_path=processed_path,
        status_value="completed",
        model_name="RDNet",
        mode="balanced",
        image_size=f"{os.path.getsize(processed_path) / (1024 * 1024):.2f} MB",
        processing_time=0.0,
        original_filename="Sample Architectural Image",
        stored_filename=os.path.basename(original_path),
        mime_type="image/jpeg",
        file_size=os.path.getsize(original_path),
        width=width,
        height=height,
        source="dashboard",
        active_workspace=True,
        thumbnail_path=processed_path,
    )
    set_active_workspace_prediction(db, user.id, prediction.id)
    create_edit_version(
        db,
        user_id=user.id,
        image_id=prediction.id,
        project_id=None,
        version_name="Original Upload",
        version_type="original",
        file_path=original_path,
        is_active=False,
    )
    create_edit_version(
        db,
        user_id=user.id,
        image_id=prediction.id,
        project_id=None,
        version_name="Balanced Restore",
        version_type="processed",
        file_path=processed_path,
        is_active=True,
    )
    from app.services.dashboard_service import build_workspace_payload

    return build_workspace_payload(db, user)
