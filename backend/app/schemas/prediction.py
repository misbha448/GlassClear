from pydantic import BaseModel
from datetime import datetime


class PredictionResponse(BaseModel):
    id: int
    user_id: int | None
    original_image_path: str
    output_image_path: str | None
    status: str
    model_name: str
    processing_mode: str
    image_size: str | None
    is_favorite: bool
    processing_time: float | None
    created_at: datetime

    model_config = {
        "from_attributes": True
    }