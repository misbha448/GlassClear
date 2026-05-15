from datetime import datetime

from pydantic import BaseModel


class BatchItemResponse(BaseModel):
    id: int
    image_id: int
    filename: str
    status: str
    original_url: str | None = None
    processed_url: str | None = None
    error_message: str | None = None
    created_at: datetime | None = None


class BatchUploadResponse(BaseModel):
    batch_id: int
    status: str
    total_count: int
    items: list[BatchItemResponse]


class BatchStartResponse(BaseModel):
    success: bool = True
    batch_id: int
    status: str
    message: str


class BatchStatusResponse(BaseModel):
    batch_id: int
    status: str
    total_count: int
    completed_count: int
    failed_count: int
    items: list[BatchItemResponse]
    zip_url: str | None = None
