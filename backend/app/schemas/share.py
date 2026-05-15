from datetime import datetime

from pydantic import BaseModel


class ShareCreateRequest(BaseModel):
    image_id: int | None = None
    prediction_id: int | None = None
    title: str | None = None
    allow_download: bool = True
    expires_in_days: int | None = None


class ShareCreateResponse(BaseModel):
    id: int | None = None
    public_url: str | None = None
    share_url: str
    token: str
    expires_at: datetime | None = None
    status: str | None = None


class PublicShareResponse(BaseModel):
    id: int | None = None
    token: str | None = None
    title: str
    filename: str | None = None
    original_url: str | None = None
    processed_url: str | None = None
    comparison_url: str | None = None
    created_at: datetime
    status: str | None = None
    owner_name: str | None = None
    expires_at: datetime | None = None
