from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.services.dashboard_service import get_album_detail_payload, get_smart_albums_payload

router = APIRouter(prefix="/api/albums", tags=["albums"])


@router.get("")
def list_albums(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_smart_albums_payload(db, current_user)


@router.get("/{album_id}")
def get_album(album_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_album_detail_payload(db, current_user, album_id)
