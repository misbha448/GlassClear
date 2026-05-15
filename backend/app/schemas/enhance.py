from pydantic import BaseModel


class EnhanceRequest(BaseModel):
    prediction_id: int


class EnhanceResponse(BaseModel):
    enhanced_image_url: str
