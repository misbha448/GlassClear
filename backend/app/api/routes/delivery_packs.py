from pydantic import BaseModel
from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.services.delivery_pack_service import create_delivery_pack_payload, get_delivery_pack_download_payload

router = APIRouter(prefix="/api/delivery-packs", tags=["delivery-packs"])


class CreateDeliveryPackRequest(BaseModel):
    prediction_id: int


@router.post("")
def create_delivery_pack(
    payload: CreateDeliveryPackRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_delivery_pack_payload(db, current_user, payload.prediction_id)


@router.get("/{pack_id}/download")
def download_delivery_pack(
    pack_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    file_path, filename, media_type = get_delivery_pack_download_payload(db, current_user, pack_id)
    return FileResponse(path=file_path, media_type=media_type, filename=filename)
