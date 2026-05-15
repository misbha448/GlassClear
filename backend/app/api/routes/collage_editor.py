from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.collage import CollageCreateRequest
from app.services.collage_service import create_collage, delete_collage, list_collages

router = APIRouter(prefix="/api/collage", tags=["collage-editor"])


@router.post("/create")
def create_new_collage(payload: CollageCreateRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_collage(db, current_user, payload.layout_type, payload.title, payload.image_ids, payload.images)


@router.get("/list")
def get_collages(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return list_collages(db, current_user)


@router.delete("/{collage_id}")
def remove_collage(collage_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return delete_collage(db, current_user, collage_id)
