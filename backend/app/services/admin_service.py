from __future__ import annotations

import os
from datetime import date, datetime, timedelta
from pathlib import Path

from fastapi import HTTPException
from sqlalchemy import func, inspect, or_, text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.batch_job import BatchJob, BatchJobItem
from app.models.edit_version import EditVersion
from app.models.prediction import Prediction
from app.models.project import Project
from app.models.share_link import ShareLink
from app.models.user import User
from app.services.dashboard_service import file_path_to_url

VALID_JOB_STATUSES = {"completed", "failed", "processing", "queued"}
VALID_USER_STATUSES = {"active", "disabled"}


def _bind_inspector(db: Session):
    bind = db.get_bind()
    return inspect(bind) if bind is not None else None


def _table_exists(db: Session, table_name: str) -> bool:
    inspector = _bind_inspector(db)
    return inspector is not None and table_name in set(inspector.get_table_names())


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _uploads_root() -> Path:
    return (_project_root() / "uploads").resolve()


def _safe_resolve_upload(path_value: str | None) -> Path | None:
    if not path_value:
        return None
    path = Path(path_value)
    if not path.is_absolute():
        path = (_project_root() / path).resolve()
    else:
        path = path.resolve()
    try:
        path.relative_to(_uploads_root())
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Unsafe file path detected") from exc
    return path


def _safe_delete_upload(path_value: str | None) -> None:
    target = _safe_resolve_upload(path_value)
    if target and target.exists() and target.is_file():
        target.unlink()


def _status_is_admin(user: User) -> bool:
    return bool(getattr(user, "is_admin", False) or getattr(user, "role", None) == "admin")


def _normalize_job_status(value: str | None) -> str:
    normalized = (value or "").strip().lower()
    if normalized in {"pending", "queued"}:
        return "queued"
    if normalized in {"processing", "running", "in_progress"}:
        return "processing"
    if normalized == "success":
        return "completed"
    return normalized or "queued"


def _to_storage_mb(value: int | float | None) -> float:
    if not value:
        return 0.0
    return round(float(value) / (1024 * 1024), 2)


def _compute_storage_used_mb(db: Session) -> float:
    file_size_total = db.query(func.coalesce(func.sum(Prediction.file_size), 0)).scalar() or 0
    if file_size_total:
        return _to_storage_mb(file_size_total)

    uploads_root = _uploads_root()
    total = 0
    if uploads_root.exists():
        for path in uploads_root.rglob("*"):
            if path.is_file():
                try:
                    total += path.stat().st_size
                except OSError:
                    continue
    return _to_storage_mb(total)


def _avg_processing_time(db: Session) -> float:
    avg_value = (
        db.query(func.avg(Prediction.processing_time))
        .filter(Prediction.processing_time.isnot(None))
        .scalar()
    )
    return round(float(avg_value), 2) if avg_value else 0.0


def _user_last_activity(db: Session, user_id: int, fallback: datetime | None) -> datetime | None:
    timestamps = []
    latest_prediction = db.query(func.max(Prediction.updated_at)).filter(Prediction.user_id == user_id).scalar()
    latest_batch = db.query(func.max(BatchJob.updated_at)).filter(BatchJob.user_id == user_id).scalar() if _table_exists(db, "batch_jobs") else None
    latest_share = db.query(func.max(ShareLink.created_at)).filter(ShareLink.user_id == user_id).scalar() if _table_exists(db, "share_links") else None
    latest_project = db.query(func.max(Project.updated_at)).filter(Project.user_id == user_id).scalar() if _table_exists(db, "projects") else None

    for item in (latest_prediction, latest_batch, latest_share, latest_project, fallback):
        if item:
            timestamps.append(item)
    return max(timestamps) if timestamps else None


def _serialize_user_item(db: Session, user: User) -> dict:
    total_uploads = db.query(func.count(Prediction.id)).filter(Prediction.user_id == user.id).scalar() or 0
    return {
        "id": user.id,
        "name": user.name or "Unnamed User",
        "email": user.email,
        "joined_at": user.created_at,
        "last_login": _user_last_activity(db, user.id, user.created_at),
        "total_uploads": total_uploads,
        "status": "disabled" if (user.status or "").lower() in {"disabled", "blocked", "deleted"} else "active",
        "is_admin": _status_is_admin(user),
    }


def _prediction_media_candidates(prediction: Prediction) -> list[str]:
    candidates: list[str] = []

    def add(value: str | None) -> None:
        if value and value not in candidates:
            candidates.append(value)

    add(prediction.thumbnail_path)
    add(prediction.output_image_path)
    add(prediction.original_image_path)

    for filename in (prediction.stored_filename, prediction.original_filename):
        if not filename:
            continue

        add(filename)
        add(f"uploads/{filename}")
        add(f"uploads/original/{filename}")
        add(f"uploads/output/{filename}")
        add(f"uploads/thumbnails/{filename}")

        stem = Path(filename).stem
        add(f"uploads/thumbnails/thumb_{stem}.jpg")
        add(f"uploads/output/{stem}.png")
        add(f"uploads/output/{stem}.jpg")
        add(f"uploads/output/{stem}.jpeg")

    return candidates


def _first_prediction_media_url(prediction: Prediction, *preferred_paths: str | None) -> str | None:
    checked: list[str] = []

    for value in [*preferred_paths, *_prediction_media_candidates(prediction)]:
        if not value or value in checked:
            continue
        checked.append(value)

        url = file_path_to_url(value)
        if url:
            return url

    return None


def _serialize_job_item(prediction: Prediction, user: User | None) -> dict:
    filename = prediction.original_filename or prediction.stored_filename or f"Job {prediction.id}"
    return {
        "id": prediction.id,
        "filename": filename,
        "user_name": user.name if user else "Guest",
        "user_email": user.email if user else None,
        "status": _normalize_job_status(prediction.status),
        "processing_time": round(float(prediction.processing_time), 2) if prediction.processing_time is not None else None,
        "created_at": prediction.created_at,
        "thumbnail_url": _first_prediction_media_url(
            prediction,
            prediction.thumbnail_path,
            prediction.output_image_path,
            prediction.original_image_path,
        ),
        "original_url": _first_prediction_media_url(prediction, prediction.original_image_path),
        "processed_url": _first_prediction_media_url(prediction, prediction.output_image_path, prediction.original_image_path),
    }


def _serialize_share_item(share: ShareLink, user: User | None, prediction: Prediction | None) -> dict:
    filename = None
    if prediction:
        filename = prediction.original_filename or prediction.stored_filename or f"Image {prediction.id}"
    status = "disabled" if share.expires_at and share.expires_at <= datetime.utcnow() else "active"
    return {
        "id": share.id,
        "title": share.title or "GlassClear Result",
        "user_name": user.name if user else "Unknown User",
        "image_filename": filename,
        "token": share.token,
        "created_at": share.created_at,
        "status": status,
        "share_url": f"{settings.FRONTEND_URL.rstrip('/')}/share/{share.token}",
    }


def _day_range(days: int = 7) -> tuple[date, date]:
    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=days - 1)
    return start_date, end_date


def _generate_date_series(start_date: date, end_date: date) -> list[date]:
    current = start_date
    points: list[date] = []
    while current <= end_date:
        points.append(current)
        current += timedelta(days=1)
    return points


def _remove_prediction_relations(db: Session, prediction: Prediction) -> None:
    db.query(ShareLink).filter(ShareLink.image_id == prediction.id).delete(synchronize_session=False)
    if _table_exists(db, "batch_job_items"):
        db.query(BatchJobItem).filter(BatchJobItem.image_id == prediction.id).delete(synchronize_session=False)
    if _table_exists(db, "edit_versions"):
        versions = db.query(EditVersion).filter(EditVersion.image_id == prediction.id).all()
        for version in versions:
            _safe_delete_upload(version.file_path)
            db.delete(version)
    if _table_exists(db, "projects"):
        db.query(Project).filter(Project.cover_image_id == prediction.id).update({Project.cover_image_id: None}, synchronize_session=False)


class AdminService:
    @staticmethod
    def get_overview(db: Session) -> dict:
        total_users = (
            db.query(func.count(User.id))
            .filter(or_(User.status.is_(None), User.status != "deleted"))
            .scalar()
            or 0
        )
        total_images_processed = db.query(func.count(Prediction.id)).filter(Prediction.status == "completed").scalar() or 0
        successful_jobs = db.query(func.count(Prediction.id)).filter(Prediction.status == "completed").scalar() or 0
        failed_jobs = db.query(func.count(Prediction.id)).filter(Prediction.status == "failed").scalar() or 0
        active_batch_jobs = (
            db.query(func.count(BatchJob.id))
            .filter(BatchJob.status.in_(["queued", "processing"]))
            .scalar()
            or 0
        )
        total_share_links = db.query(func.count(ShareLink.id)).scalar() or 0

        return {
            "stats": {
                "total_users": total_users,
                "total_images_processed": total_images_processed,
                "successful_jobs": successful_jobs,
                "failed_jobs": failed_jobs,
                "active_batch_jobs": active_batch_jobs,
                "total_share_links": total_share_links,
                "storage_used_mb": _compute_storage_used_mb(db),
                "avg_processing_time_sec": _avg_processing_time(db),
            }
        }

    @staticmethod
    def get_analytics(db: Session) -> dict:
        start_date, end_date = _day_range(7)
        start_dt = datetime.combine(start_date, datetime.min.time())

        upload_rows = (
            db.query(func.date(Prediction.created_at).label("day"), func.count(Prediction.id))
            .filter(Prediction.created_at >= start_dt)
            .group_by(func.date(Prediction.created_at))
            .all()
        )
        completed_rows = (
            db.query(func.date(Prediction.created_at).label("day"), func.count(Prediction.id))
            .filter(Prediction.created_at >= start_dt, Prediction.status == "completed")
            .group_by(func.date(Prediction.created_at))
            .all()
        )
        failed_rows = (
            db.query(func.date(Prediction.created_at).label("day"), func.count(Prediction.id))
            .filter(Prediction.created_at >= start_dt, Prediction.status == "failed")
            .group_by(func.date(Prediction.created_at))
            .all()
        )
        share_rows = (
            db.query(func.date(ShareLink.created_at).label("day"), func.count(ShareLink.id))
            .filter(ShareLink.created_at >= start_dt)
            .group_by(func.date(ShareLink.created_at))
            .all()
        )
        user_rows = (
            db.query(func.date(User.created_at).label("day"), func.count(User.id))
            .filter(User.created_at >= start_dt)
            .group_by(func.date(User.created_at))
            .all()
        )

        upload_map = {str(day): count for day, count in upload_rows}
        completed_map = {str(day): count for day, count in completed_rows}
        failed_map = {str(day): count for day, count in failed_rows}
        share_map = {str(day): count for day, count in share_rows}
        user_map = {str(day): count for day, count in user_rows}

        weekly_processing = []
        share_activity = []
        user_growth = []
        for day in _generate_date_series(start_date, end_date):
            key = day.isoformat()
            weekly_processing.append(
                {
                    "date": key,
                    "uploads": int(upload_map.get(key, 0)),
                    "completed": int(completed_map.get(key, 0)),
                    "failed": int(failed_map.get(key, 0)),
                }
            )
            share_activity.append({"date": key, "shares": int(share_map.get(key, 0))})
            user_growth.append({"date": key, "users": int(user_map.get(key, 0))})

        distribution = {"completed": 0, "failed": 0, "processing": 0, "queued": 0}
        status_rows = db.query(Prediction.status, func.count(Prediction.id)).group_by(Prediction.status).all()
        for raw_status, count in status_rows:
            normalized = _normalize_job_status(raw_status)
            if normalized in distribution:
                distribution[normalized] += int(count)

        return {
            "weekly_processing": weekly_processing,
            "status_distribution": distribution,
            "share_activity": share_activity,
            "user_growth": user_growth,
        }

    @staticmethod
    def get_users(db: Session, search: str | None, status: str | None, limit: int, offset: int) -> dict:
        query = db.query(User).filter(or_(User.status.is_(None), User.status != "deleted"))
        if search:
            term = f"%{search.strip()}%"
            query = query.filter(or_(User.name.ilike(term), User.email.ilike(term)))
        if status:
            normalized_status = status.strip().lower()
            if normalized_status == "active":
                query = query.filter(or_(User.status.is_(None), User.status == "active"))
            elif normalized_status == "disabled":
                query = query.filter(User.status.in_(["disabled", "blocked"]))
        total = query.count()
        users = query.order_by(User.created_at.desc(), User.id.desc()).offset(offset).limit(limit).all()
        return {"items": [_serialize_user_item(db, user) for user in users], "total": total}

    @staticmethod
    def get_user_detail(db: Session, user_id: int) -> dict:
        user = (
            db.query(User)
            .filter(User.id == user_id, or_(User.status.is_(None), User.status != "deleted"))
            .first()
        )
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        payload = _serialize_user_item(db, user)
        recent_predictions = (
            db.query(Prediction)
            .filter(Prediction.user_id == user.id)
            .order_by(Prediction.created_at.desc(), Prediction.id.desc())
            .limit(5)
            .all()
        )
        payload["recent_jobs"] = [_serialize_job_item(prediction, user) for prediction in recent_predictions]
        return payload

    @staticmethod
    def update_user_status(db: Session, user_id: int, status: str, current_admin: User) -> dict:
        if status not in VALID_USER_STATUSES:
            raise HTTPException(status_code=400, detail="Invalid status")

        user = (
            db.query(User)
            .filter(User.id == user_id, or_(User.status.is_(None), User.status != "deleted"))
            .first()
        )
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if user.id == current_admin.id:
            raise HTTPException(status_code=400, detail="You cannot disable your own account")

        user.status = status
        db.commit()
        db.refresh(user)
        return AdminService.get_user_detail(db, user.id)

    @staticmethod
    def delete_user(db: Session, user_id: int, current_admin: User) -> dict:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if user.id == current_admin.id:
            raise HTTPException(status_code=400, detail="You cannot delete your own account")

        user.status = "deleted"
        db.commit()
        return {"success": True, "message": "User deleted successfully."}

    @staticmethod
    def get_jobs(db: Session, status: str | None, search: str | None, limit: int, offset: int) -> dict:
        if status and status not in VALID_JOB_STATUSES:
            raise HTTPException(status_code=400, detail="Invalid status filter")

        query = db.query(Prediction, User).outerjoin(User, Prediction.user_id == User.id)
        if status:
            if status == "queued":
                query = query.filter(Prediction.status.in_(["queued", "pending"]))
            elif status == "processing":
                query = query.filter(Prediction.status.in_(["processing", "running", "in_progress"]))
            else:
                query = query.filter(Prediction.status == status)
        if search:
            term = f"%{search.strip()}%"
            query = query.filter(
                or_(
                    Prediction.original_filename.ilike(term),
                    Prediction.stored_filename.ilike(term),
                    User.name.ilike(term),
                    User.email.ilike(term),
                )
            )

        total = query.count()
        rows = query.order_by(Prediction.created_at.desc(), Prediction.id.desc()).offset(offset).limit(limit).all()
        return {"items": [_serialize_job_item(prediction, user) for prediction, user in rows], "total": total}

    @staticmethod
    def delete_job(db: Session, job_id: int) -> dict:
        prediction = db.query(Prediction).filter(Prediction.id == job_id).first()
        if not prediction:
            raise HTTPException(status_code=404, detail="Job not found")

        _remove_prediction_relations(db, prediction)
        for path_value in {prediction.original_image_path, prediction.output_image_path, prediction.thumbnail_path}:
            _safe_delete_upload(path_value)
        db.delete(prediction)
        db.commit()
        return {"success": True, "message": "Job deleted successfully."}

    @staticmethod
    def reprocess_job(db: Session, job_id: int) -> dict:
        prediction = db.query(Prediction).filter(Prediction.id == job_id).first()
        if not prediction:
            raise HTTPException(status_code=404, detail="Job not found")
        raise HTTPException(status_code=501, detail="Reprocess is not connected yet.")

    @staticmethod
    def get_shares(db: Session, limit: int, offset: int) -> dict:
        rows = (
            db.query(ShareLink, User, Prediction)
            .outerjoin(User, ShareLink.user_id == User.id)
            .outerjoin(Prediction, ShareLink.image_id == Prediction.id)
            .order_by(ShareLink.created_at.desc(), ShareLink.id.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )
        total = db.query(func.count(ShareLink.id)).scalar() or 0
        return {
            "items": [_serialize_share_item(share, user, prediction) for share, user, prediction in rows],
            "total": total,
        }

    @staticmethod
    def disable_share(db: Session, share_id: int) -> dict:
        share = db.query(ShareLink).filter(ShareLink.id == share_id).first()
        if not share:
            raise HTTPException(status_code=404, detail="Share link not found")
        share.expires_at = datetime.utcnow()
        db.commit()
        return {"success": True, "message": "Share link disabled successfully."}

    @staticmethod
    def delete_share(db: Session, share_id: int) -> dict:
        share = db.query(ShareLink).filter(ShareLink.id == share_id).first()
        if not share:
            raise HTTPException(status_code=404, detail="Share link not found")
        db.delete(share)
        db.commit()
        return {"success": True, "message": "Share link deleted successfully."}

    @staticmethod
    def get_system_health(db: Session) -> dict:
        try:
            db.execute(text("SELECT 1"))
            database_status = "connected"
        except Exception:
            database_status = "error"

        ml_model_status = "loaded" if (_project_root() / "app" / "rdnet_infer.py").exists() else "available"
        failed_jobs_count = db.query(func.count(Prediction.id)).filter(Prediction.status == "failed").scalar() or 0
        active_batch_jobs = (
            db.query(func.count(BatchJob.id))
            .filter(BatchJob.status.in_(["queued", "processing"]))
            .scalar()
            or 0
        )

        return {
            "api_status": "online",
            "ml_model_status": ml_model_status,
            "database_status": database_status,
            "storage_used_mb": _compute_storage_used_mb(db),
            "avg_processing_time_sec": _avg_processing_time(db),
            "failed_jobs_count": failed_jobs_count,
            "active_batch_jobs": active_batch_jobs,
        }

    @staticmethod
    def clear_failed_jobs(db: Session) -> dict:
        failed_predictions = db.query(Prediction).filter(Prediction.status == "failed").all()
        cleared = 0
        for prediction in failed_predictions:
            _remove_prediction_relations(db, prediction)
            for path_value in {prediction.original_image_path, prediction.output_image_path, prediction.thumbnail_path}:
                _safe_delete_upload(path_value)
            db.delete(prediction)
            cleared += 1
        db.commit()
        return {"success": True, "message": "Failed jobs cleared successfully.", "count": cleared}

    @staticmethod
    def cleanup_expired_shares(db: Session) -> dict:
        now = datetime.utcnow()
        expired_shares = db.query(ShareLink).filter(ShareLink.expires_at.isnot(None), ShareLink.expires_at <= now).all()
        cleaned = 0
        for share in expired_shares:
            db.delete(share)
            cleaned += 1
        db.commit()
        return {"success": True, "message": "Expired shares cleaned successfully.", "count": cleaned}
