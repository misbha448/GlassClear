from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ClaimGuestImageRequest(BaseModel):
    guest_image_token: str


class DashboardImageItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    filename: str
    original_url: str | None = None
    processed_url: str | None = None
    status: str
    category: str | None = None
    created_at: datetime


class WorkspaceStats(BaseModel):
    total_processed: int
    total_batches: int
    shared_links: int


class WorkspaceResponse(BaseModel):
    latest_result: DashboardImageItem | None = None
    stats: WorkspaceStats


class HistoryResponse(BaseModel):
    items: list[DashboardImageItem]


class SmartAlbum(BaseModel):
    slug: str
    name: str
    description: str
    count: int
    cover_url: str | None = None
    updated_at: datetime | None = None


class SmartAlbumsResponse(BaseModel):
    albums: list[SmartAlbum]
