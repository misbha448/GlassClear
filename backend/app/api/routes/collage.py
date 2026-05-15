from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.prediction_service import get_prediction_by_id
from app.utils.collage_generator import create_smart_collage
from app.api.deps import get_current_user_optional
from app.models.user import User
from typing import Optional, List

router = APIRouter(prefix="/api/v1/collage", tags=["collage"])

@router.post("/generate")
async def generate_collage(
    image_ids: List[int] = Body(...),
    layout: str = Body("Grid"),
    bg_color: str = Body("#08080e"),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    image_paths = []
    for img_id in image_ids:
        prediction = get_prediction_by_id(db=db, prediction_id=img_id, user_id=current_user.id if current_user else None)
        if prediction and prediction.output_image_path:
            image_paths.append(prediction.output_image_path)
    
    if not image_paths:
        raise HTTPException(status_code=404, detail="No valid processed images found for collage")
    
    result_path = create_smart_collage(image_paths, layout, bg_color)
    if not result_path:
        raise HTTPException(status_code=500, detail="Collage generation failed")
        
    return {"collage_url": f"/{result_path}"}