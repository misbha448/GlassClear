from fastapi import APIRouter, Depends, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.services.delivery_service import create_export_asset
from app.services.prediction_service import get_prediction_by_id

router = APIRouter(prefix="/api/export", tags=["export"])


@router.get("/{image_id}")
def export_image_file(
    image_id: int,
    format: str = Query(default="png"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    prediction = get_prediction_by_id(db, image_id, current_user.id)
    export_path, filename, media_type = create_export_asset(prediction, format)
    return FileResponse(path=export_path, media_type=media_type, filename=filename)
