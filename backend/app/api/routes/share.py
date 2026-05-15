import mimetypes

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.share import ShareCreateRequest
from app.services.share_service import (
    create_share_link,
    delete_share_link,
    get_public_share,
    get_public_share_comparison,
    get_user_share_comparison,
    list_share_links,
)

router = APIRouter(prefix="/api/share", tags=["share"])
share_links_router = APIRouter(prefix="/api/share-links", tags=["share"])


def _prediction_id_from_payload(payload: ShareCreateRequest) -> int:
    prediction_id = payload.prediction_id or payload.image_id
    if not prediction_id:
        raise HTTPException(status_code=400, detail="prediction_id is required")
    return prediction_id


@router.post("")
@router.post("/links")
def create_share_v2(payload: ShareCreateRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    prediction_id = _prediction_id_from_payload(payload)
    return create_share_link(db, current_user, prediction_id, payload.title, payload.allow_download, payload.expires_in_days)


@router.post("/create")
def create_share(payload: ShareCreateRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    prediction_id = _prediction_id_from_payload(payload)
    return create_share_link(db, current_user, prediction_id, payload.title, payload.allow_download, payload.expires_in_days)


@share_links_router.post("")
def create_share_links_alias(payload: ShareCreateRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    prediction_id = _prediction_id_from_payload(payload)
    return create_share_link(db, current_user, prediction_id, payload.title, payload.allow_download, payload.expires_in_days)


@router.get("/list")
def list_shares(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return list_share_links(db, current_user)


@router.get("/public/{token}")
def public_share(token: str, db: Session = Depends(get_db)):
    return get_public_share(db, token)


@share_links_router.get("/public/{token}")
def public_share_links_alias(token: str, db: Session = Depends(get_db)):
    return get_public_share(db, token)


@router.get("/public/{token}/comparison")
def public_share_comparison(token: str, db: Session = Depends(get_db)):
    comparison_path, filename = get_public_share_comparison(db, token)
    media_type = mimetypes.guess_type(comparison_path)[0] or "image/jpeg"
    return FileResponse(path=comparison_path, media_type=media_type, filename=filename)


@router.get("/comparison/{image_id}")
def download_share_comparison(image_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    comparison_path, filename = get_user_share_comparison(db, current_user, image_id)
    media_type = mimetypes.guess_type(comparison_path)[0] or "image/jpeg"
    return FileResponse(path=comparison_path, media_type=media_type, filename=filename)


@router.delete("/{share_id}")
def remove_share(share_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return delete_share_link(db, current_user, share_id)


@router.get("/{token}")
def public_share_v2(token: str, db: Session = Depends(get_db)):
    return get_public_share(db, token)
