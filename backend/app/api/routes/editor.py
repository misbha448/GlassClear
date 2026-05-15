from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.editor import ApplyReflectionRequest, ApplyToolRequest, ExportRequest
from app.services.editor_service import (
    activate_version,
    apply_tool,
    download_image,
    export_image,
    get_current_image,
    get_recent_edits,
    get_versions_for_image,
    set_current_image,
    upload_editor_image,
)

router = APIRouter(prefix="/api/editor", tags=["editor"])


@router.get("/current-image")
def current_image(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_current_image(db, current_user)


@router.put("/current-image/{image_id}")
def update_current_image(image_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return set_current_image(db, current_user, image_id)


@router.post("/upload")
def upload_image(
    file: UploadFile = File(...),
    project_id: int | None = Form(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return upload_editor_image(db, current_user, file, project_id)


@router.post("/apply-tool")
def apply_editor_tool(payload: ApplyToolRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return apply_tool(db, current_user, payload.image_id, payload.tool, payload.settings or {})


@router.post("/apply-reflection")
def apply_editor_reflection(payload: ApplyReflectionRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return apply_tool(db, current_user, payload.image_id, "remove_reflection", payload.settings or {})


@router.get("/images/{image_id}/versions")
def get_image_versions(image_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_versions_for_image(db, current_user, image_id)


@router.put("/versions/{version_id}/activate")
def activate_image_version(version_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return activate_version(db, current_user, version_id)


@router.get("/recent-edits")
def recent_edits(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_recent_edits(db, current_user)


@router.get("/images/{image_id}/download")
def download_editor_image(image_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return download_image(db, current_user, image_id)


@router.post("/export")
def export_editor_image(payload: ExportRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    export_kind = payload.export_type or payload.type or "processed"
    return export_image(db, current_user, payload.image_id, export_kind)
