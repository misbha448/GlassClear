from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.dashboard import ClaimGuestImageRequest
from app.services.dashboard_service import (
    build_workspace_payload,
    delete_history_item,
    get_album_detail_payload,
    get_dashboard_result_payload,
    get_filtered_tools,
    get_history_payload,
    get_smart_albums_payload,
)
from app.services.editor_service import claim_guest_image, get_demo_image_payload, use_demo_image
from app.services.project_service import list_projects

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/workspace")
def get_workspace(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return build_workspace_payload(db, current_user)


@router.get("/workspace/images/{image_id}")
def get_workspace_image(image_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_dashboard_result_payload(db, current_user, image_id)


@router.get("/history")
def get_history(
    limit: int | None = Query(default=None, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    status: str | None = Query(default=None),
    search: str | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_history_payload(db, current_user, limit=limit, offset=offset, status=status, search=search)


@router.delete("/history/{image_id}")
def remove_history_item(image_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return delete_history_item(db, current_user, image_id)


@router.get("/smart-albums")
def get_smart_albums(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_smart_albums_payload(db, current_user)


@router.get("/albums")
def get_dashboard_albums(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_smart_albums_payload(db, current_user)


@router.get("/albums/{album_slug}")
def get_dashboard_album(album_slug: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_album_detail_payload(db, current_user, album_slug)


@router.get("/my-projects")
def get_my_projects(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return {"projects": list_projects(db, current_user)}


@router.get("/tools")
def get_tools(search: str | None = Query(default=None)):
    return {"tools": get_filtered_tools(search)}


@router.post("/claim-guest-image")
def claim_guest(payload: ClaimGuestImageRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return claim_guest_image(db, current_user, payload.guest_image_token)


@router.get("/demo-image")
def get_demo_image():
    return get_demo_image_payload()


@router.post("/use-demo-image")
def activate_demo_image(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return use_demo_image(db, current_user)
