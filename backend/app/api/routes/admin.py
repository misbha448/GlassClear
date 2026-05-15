from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.admin import (
    AdminActionResponse,
    AdminAnalyticsResponse,
    AdminJobItem,
    AdminJobListResponse,
    AdminOverviewResponse,
    AdminShareListResponse,
    AdminSystemHealthResponse,
    AdminUserDetail,
    AdminUserListResponse,
    AdminUserStatusUpdate,
)
from app.services.admin_service import AdminService

router = APIRouter(prefix="/api/admin", tags=["Admin"])


@router.get("/overview", response_model=AdminOverviewResponse)
def get_admin_overview(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin_user),
):
    return AdminService.get_overview(db)


@router.get("/analytics", response_model=AdminAnalyticsResponse)
def get_admin_analytics(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin_user),
):
    return AdminService.get_analytics(db)


@router.get("/users", response_model=AdminUserListResponse)
def get_admin_users(
    search: str | None = Query(default=None),
    status: str | None = Query(default=None),
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin_user),
):
    return AdminService.get_users(db, search=search, status=status, limit=limit, offset=offset)


@router.get("/users/{user_id}", response_model=AdminUserDetail)
def get_admin_user_detail(
    user_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin_user),
):
    return AdminService.get_user_detail(db, user_id)


@router.patch("/users/{user_id}/status", response_model=AdminUserDetail)
def update_admin_user_status(
    user_id: int,
    payload: AdminUserStatusUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
):
    return AdminService.update_user_status(db, user_id, payload.status, current_admin)


@router.delete("/users/{user_id}", response_model=AdminActionResponse)
def delete_admin_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
):
    return AdminService.delete_user(db, user_id, current_admin)


@router.get("/jobs", response_model=AdminJobListResponse)
def get_admin_jobs(
    status: str | None = Query(default=None),
    search: str | None = Query(default=None),
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin_user),
):
    return AdminService.get_jobs(db, status=status, search=search, limit=limit, offset=offset)


@router.delete("/jobs/{job_id}", response_model=AdminActionResponse)
def delete_admin_job(
    job_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin_user),
):
    return AdminService.delete_job(db, job_id)


@router.post("/jobs/{job_id}/reprocess", response_model=AdminActionResponse | AdminJobItem)
def reprocess_admin_job(
    job_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin_user),
):
    return AdminService.reprocess_job(db, job_id)


@router.get("/shares", response_model=AdminShareListResponse)
def get_admin_shares(
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin_user),
):
    return AdminService.get_shares(db, limit=limit, offset=offset)


@router.patch("/shares/{share_id}/disable", response_model=AdminActionResponse)
def disable_admin_share(
    share_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin_user),
):
    return AdminService.disable_share(db, share_id)


@router.delete("/shares/{share_id}", response_model=AdminActionResponse)
def delete_admin_share(
    share_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin_user),
):
    return AdminService.delete_share(db, share_id)


@router.get("/system-health", response_model=AdminSystemHealthResponse)
def get_admin_system_health(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin_user),
):
    return AdminService.get_system_health(db)


@router.post("/maintenance/clear-failed-jobs", response_model=AdminActionResponse)
def clear_failed_jobs(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin_user),
):
    return AdminService.clear_failed_jobs(db)


@router.post("/maintenance/cleanup-expired-shares", response_model=AdminActionResponse)
def cleanup_expired_shares(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin_user),
):
    return AdminService.cleanup_expired_shares(db)

