from pydantic import BaseModel


class VariationRequest(BaseModel):
    prediction_id: int


class VariationItem(BaseModel):
    key: str
    label: str
    image_url: str


class VariationResponse(BaseModel):
    variations: list[VariationItem]
