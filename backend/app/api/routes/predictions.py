from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import Optional, List
import mimetypes
import os

from app.core.database import get_db
from app.api.deps import get_current_user, get_current_user_optional
from app.models.user import User
from app.services.prediction_service import get_prediction_by_id, get_user_predictions, get_user_stats
from app.schemas.prediction import PredictionResponse

router = APIRouter(
    prefix="/api/v1/predictions",
    tags=["predictions"],
)

@router.get("/", response_model=List[PredictionResponse])
async def list_user_predictions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Fetch all history for the logged-in user."""
    return get_user_predictions(db=db, user_id=current_user.id)

@router.get("/stats")
async def get_dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Fetch stats like 'Processed This Week' for the dashboard."""
    return get_user_stats(db=db, user_id=current_user.id)

@router.get("/{prediction_id}/download")
async def download_prediction(
    prediction_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    # The `get_prediction_by_id` service function now handles the authorization logic
    # based on whether current_user is authenticated or a guest.
    prediction = get_prediction_by_id(
        db=db,
        prediction_id=prediction_id,
        user_id=current_user.id if current_user else None
    )

    if not prediction.output_image_path or not os.path.exists(prediction.output_image_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Output image not found.")

    media_type, _ = mimetypes.guess_type(prediction.output_image_path)
    if not media_type:
        media_type = "application/octet-stream" # Fallback if mimetype can't be guessed

    return FileResponse(
        path=prediction.output_image_path,
        media_type=media_type,
        filename=os.path.basename(prediction.output_image_path) # Suggest a filename for download
    )

# You might have other prediction-related endpoints here, e.g.:
# @router.get("/", response_model=list[PredictionSchema])
# async def get_user_predictions_list(...):
#     # ... logic to fetch predictions for the current user ...
#     pass