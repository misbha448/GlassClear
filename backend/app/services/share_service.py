from __future__ import annotations

import secrets
from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.prediction import Prediction
from app.models.share_link import ShareLink
from app.models.user import User
from app.services.delivery_service import create_comparison_export
from app.services.dashboard_service import file_path_to_url
from app.services.prediction_service import get_prediction_by_id


def _public_share_url(token: str) -> str:
    return f"{settings.FRONTEND_URL.rstrip('/')}/share/{token}"


def create_share_link(db: Session, user: User, image_id: int, title: str | None, allow_download: bool, expires_in_days: int | None) -> dict:
    print(f"share.create prediction_id={image_id} current_user_id={user.id}")
    prediction = get_prediction_by_id(db, image_id, user.id)
    if not prediction.output_image_path and not prediction.original_image_path:
        raise HTTPException(status_code=404, detail="Image not found")

    share = (
        db.query(ShareLink)
        .filter(ShareLink.user_id == user.id, ShareLink.image_id == prediction.id, ShareLink.is_active.is_(True))
        .order_by(ShareLink.created_at.desc())
        .first()
    )

    if share and share.expires_at and share.expires_at < datetime.utcnow():
        db.delete(share)
        db.commit()
        share = None

    if share:
        share.title = title or share.title or prediction.original_filename or "GlassClear Result"
        share.allow_download = allow_download
        if expires_in_days:
            share.expires_at = datetime.utcnow() + timedelta(days=expires_in_days)
        db.commit()
        db.refresh(share)
    else:
        token = secrets.token_urlsafe(32)
        expires_at = datetime.utcnow() + timedelta(days=expires_in_days) if expires_in_days else None
        share = ShareLink(
            user_id=user.id,
            image_id=prediction.id,
            project_id=prediction.project_id,
            token=token,
            title=title,
            allow_download=allow_download,
            is_active=True,
            expires_at=expires_at,
        )
        db.add(share)
        db.commit()
        db.refresh(share)

    confirmed_share = db.query(ShareLink).filter(ShareLink.token == share.token).first()
    if not confirmed_share:
        raise HTTPException(status_code=500, detail="Share link was not persisted correctly")

    print(f"share.create token={share.token} share_link_id={share.id}")

    public_url = _public_share_url(share.token)
    return {
        "id": share.id,
        "success": True,
        "token": share.token,
        "public_url": public_url,
        "share_url": public_url,
        "expires_at": share.expires_at.isoformat() if share.expires_at else None,
        "status": "active",
    }


def list_share_links(db: Session, user: User) -> dict:
    shares = db.query(ShareLink).filter(ShareLink.user_id == user.id).order_by(ShareLink.created_at.desc()).all()
    return {
        "shares": [
            {
                "id": share.id,
                "token": share.token,
                "title": share.title,
                "allow_download": share.allow_download,
                "expires_at": share.expires_at.isoformat() if share.expires_at else None,
                "public_url": _public_share_url(share.token),
                "share_url": _public_share_url(share.token),
            }
            for share in shares
        ]
    }


def get_public_share(db: Session, token: str) -> dict:
    print(f"share.public received_token={token}")
    share = db.query(ShareLink).filter(ShareLink.token == token, ShareLink.is_active.is_(True)).first()
    print(f"share.public found={bool(share)} prediction_id={share.image_id if share else None}")
    if not share:
        raise HTTPException(status_code=404, detail="Share link not found")
    if share.expires_at and share.expires_at < datetime.utcnow():
        raise HTTPException(status_code=410, detail="Share link expired")

    prediction = db.query(Prediction).filter(Prediction.id == share.image_id).first()
    if not prediction:
        raise HTTPException(status_code=404, detail="Image not found")

    owner = db.query(User).filter(User.id == share.user_id).first()
    owner_name = owner.name if owner else None

    return {
        "success": True,
        "id": share.id,
        "token": share.token,
        "title": share.title or prediction.original_filename or "GlassClear Result",
        "filename": prediction.original_filename or "GlassClear Restoration",
        "status": prediction.status,
        "original_url": file_path_to_url(prediction.original_image_path),
        "processed_url": file_path_to_url(prediction.output_image_path) or file_path_to_url(prediction.original_image_path),
        "comparison_url": f"/api/share/public/{share.token}/comparison",
        "allow_download": share.allow_download,
        "owner_name": owner_name,
        "created_at": prediction.created_at.isoformat(),
        "expires_at": share.expires_at.isoformat() if share.expires_at else None,
    }


def get_public_share_comparison(db: Session, token: str) -> tuple[str, str]:
    share = db.query(ShareLink).filter(ShareLink.token == token, ShareLink.is_active.is_(True)).first()
    if not share:
        raise HTTPException(status_code=404, detail="Share link not found")
    if share.expires_at and share.expires_at < datetime.utcnow():
        raise HTTPException(status_code=410, detail="Share link expired")

    prediction = db.query(Prediction).filter(Prediction.id == share.image_id).first()
    if not prediction:
        raise HTTPException(status_code=404, detail="Image not found")

    return create_comparison_export(prediction, share.title or prediction.original_filename or "GlassClear Result")


def get_user_share_comparison(db: Session, user: User, image_id: int) -> tuple[str, str]:
    prediction = get_prediction_by_id(db, image_id, user.id)
    return create_comparison_export(prediction, prediction.original_filename or "GlassClear Result")


def delete_share_link(db: Session, user: User, share_id: int) -> dict:
    share = db.query(ShareLink).filter(ShareLink.id == share_id, ShareLink.user_id == user.id, ShareLink.is_active.is_(True)).first()
    if not share:
        raise HTTPException(status_code=404, detail="Share link not found")
    share.is_active = False
    db.commit()
    return {"message": "Share link deleted successfully"}
