from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class AdminOverviewStats(BaseModel):
    total_users: int = 0
    total_images_processed: int = 0
    successful_jobs: int = 0
    failed_jobs: int = 0
    active_batch_jobs: int = 0
    total_share_links: int = 0
    storage_used_mb: float = 0
    avg_processing_time_sec: float = 0


class AdminOverviewResponse(BaseModel):
    stats: AdminOverviewStats


class AdminWeeklyProcessingPoint(BaseModel):
    date: str
    uploads: int = 0
    completed: int = 0
    failed: int = 0


class AdminShareActivityPoint(BaseModel):
    date: str
    shares: int = 0


class AdminUserGrowthPoint(BaseModel):
    date: str
    users: int = 0


class AdminStatusDistribution(BaseModel):
    completed: int = 0
    failed: int = 0
    processing: int = 0
    queued: int = 0


class AdminAnalyticsResponse(BaseModel):
    weekly_processing: list[AdminWeeklyProcessingPoint]
    status_distribution: AdminStatusDistribution
    share_activity: list[AdminShareActivityPoint]
    user_growth: list[AdminUserGrowthPoint]


class AdminJobBrief(BaseModel):
    id: int
    filename: str
    status: str
    processing_time: float | None = None
    created_at: datetime | None = None
    thumbnail_url: str | None = None
    original_url: str | None = None
    processed_url: str | None = None


class AdminUserItem(BaseModel):
    id: int
    name: str
    email: str
    joined_at: datetime | None = None
    last_login: datetime | None = None
    total_uploads: int = 0
    status: str = "active"
    is_admin: bool = False


class AdminUserDetail(AdminUserItem):
    recent_jobs: list[AdminJobBrief] = []


class AdminUserListResponse(BaseModel):
    items: list[AdminUserItem]
    total: int


class AdminUserStatusUpdate(BaseModel):
    status: Literal["active", "disabled"]


class AdminJobItem(BaseModel):
    id: int
    filename: str
    user_name: str | None = None
    user_email: str | None = None
    status: str
    processing_time: float | None = None
    created_at: datetime | None = None
    thumbnail_url: str | None = None
    original_url: str | None = None
    processed_url: str | None = None


class AdminJobListResponse(BaseModel):
    items: list[AdminJobItem]
    total: int


class AdminShareItem(BaseModel):
    id: int
    title: str
    user_name: str | None = None
    image_filename: str | None = None
    token: str
    created_at: datetime | None = None
    status: str
    share_url: str


class AdminShareListResponse(BaseModel):
    items: list[AdminShareItem]
    total: int


class AdminSystemHealthResponse(BaseModel):
    api_status: str
    ml_model_status: str
    database_status: str
    storage_used_mb: float = 0
    avg_processing_time_sec: float = 0
    failed_jobs_count: int = 0
    active_batch_jobs: int = 0


class AdminActionResponse(BaseModel):
    success: bool = True
    message: str
    count: int | None = None

