from pydantic import BaseModel


class StoryRequest(BaseModel):
    prediction_id: int
    ai_mode: str = "fidelity"
    ssim: float = 0.0
    edge_score: float = 0.0
    ai_reason: str = ""


class StoryResponse(BaseModel):
    story: str
