import mimetypes
import os

from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.services.batch_service import get_batch, get_batch_zip_path, list_batches, start_batch, upload_batch

router = APIRouter(prefix="/api/batch", tags=["batch"])


@router.post("/upload")
def create_batch_upload(
    files: list[UploadFile] = File(...),
    project_id: int | None = Form(default=None),
    tool: str = Form(default="remove_reflection"),
    settings: str | None = Form(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return upload_batch(db, current_user, files, project_id, tool, settings)


@router.post("/{batch_id}/start")
def start_batch_processing(
    batch_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return start_batch(db, current_user, batch_id, background_tasks)


@router.get("/{batch_id}")
def fetch_batch(batch_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_batch(db, current_user, batch_id)


@router.get("/{batch_id}/download-zip")
def download_batch_zip(batch_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    zip_path = get_batch_zip_path(db, current_user, batch_id)
    media_type = mimetypes.guess_type(zip_path)[0] or "application/zip"
    return FileResponse(path=zip_path, media_type=media_type, filename=os.path.basename(zip_path))


@router.get("")
def fetch_batches(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return list_batches(db, current_user)
