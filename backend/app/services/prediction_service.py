import os
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status

from app.models.prediction import Prediction
from app.models.collection import CollectionItem
from app.models.delivery_pack import DeliveryPack


def create_prediction(
    db: Session,
    user_id: int | None,
    original_image_path: str,
    output_image_path: str | None,
    status_value: str = "completed",
    model_name: str = "XReflection",
    mode: str = "fidelity",
    image_size: str | None = None,
    processing_time: float | None = None,
    project_id: int | None = None,
    original_filename: str | None = None,
    stored_filename: str | None = None,
    mime_type: str | None = None,
    file_size: int | None = None,
    width: int | None = None,
    height: int | None = None,
    source: str = "dashboard",
    guest_image_token: str | None = None,
    active_workspace: bool = False,
    thumbnail_path: str | None = None,
) -> Prediction:
    prediction = Prediction(
        user_id=user_id,
        original_image_path=original_image_path,
        output_image_path=output_image_path,
        status=status_value,
        model_name=model_name,
        processing_mode=mode,
        image_size=image_size,
        processing_time=processing_time,
        project_id=project_id,
        original_filename=original_filename,
        stored_filename=stored_filename,
        mime_type=mime_type,
        file_size=file_size,
        width=width,
        height=height,
        source=source,
        guest_image_token=guest_image_token,
        active_workspace=active_workspace,
        thumbnail_path=thumbnail_path,
    )

    db.add(prediction)
    db.commit()
    db.refresh(prediction)

    return prediction


def get_user_predictions(db: Session, user_id: int):
    return (
        db.query(Prediction)
        .filter(Prediction.user_id == user_id)
        .order_by(Prediction.created_at.desc())
        .all()
    )


def get_prediction_by_id(db: Session, prediction_id: int, user_id: int | None) -> Prediction:
    query = db.query(Prediction).filter(Prediction.id == prediction_id)

    if user_id is not None:
        # Authenticated user: must own the prediction
        query = query.filter(Prediction.user_id == user_id)
    else:
        # Guest user: can only access predictions with no associated user_id
        # This allows guests to download their own processed images.
        query = query.filter(Prediction.user_id == None)

    prediction = query.first()


    if not prediction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prediction not found"
        )

    return prediction

def toggle_favorite(db: Session, prediction_id: int, user_id: int) -> Prediction:
    """
    Toggles the is_favorite flag for a specific project.
    """
    prediction = get_prediction_by_id(db, prediction_id, user_id)
    prediction.is_favorite = not prediction.is_favorite
    db.commit()
    db.refresh(prediction)
    return prediction

def get_user_stats(db: Session, user_id: int):
    """
    Calculates data for the AI Summary dashboard section.
    """
    last_week = datetime.utcnow() - timedelta(days=7)
    
    processed_this_week = db.query(Prediction).filter(
        Prediction.user_id == user_id,
        Prediction.created_at >= last_week,
        Prediction.status == "completed"
    ).count()

    avg_time = db.query(func.avg(Prediction.processing_time)).filter(
        Prediction.user_id == user_id,
        Prediction.status == "completed"
    ).scalar() or 0.0

    # Determine the most used processing mode (Quality vs Fidelity)
    mode_counts = db.query(
        Prediction.processing_mode, func.count(Prediction.processing_mode)
    ).filter(
        Prediction.user_id == user_id
    ).group_by(Prediction.processing_mode).order_by(func.count(Prediction.processing_mode).desc()).first()

    most_used_mode = mode_counts[0] if mode_counts else "fidelity"

    return {
        "processedThisWeek": processed_this_week,
        "avgProcessingTime": f"{round(float(avg_time), 1)}s",
        "mostUsedMode": most_used_mode.capitalize()
    }

def delete_prediction(db: Session, prediction_id: int, user_id: int):
    # Reuse helper to find the record
    prediction = get_prediction_by_id(db, prediction_id, user_id)

    db.query(CollectionItem).filter(CollectionItem.prediction_id == prediction.id).delete(synchronize_session=False)
    packs = db.query(DeliveryPack).filter(DeliveryPack.prediction_id == prediction.id, DeliveryPack.user_id == user_id).all()
    for pack in packs:
        if pack.file_path and os.path.exists(pack.file_path):
            try:
                os.remove(pack.file_path)
            except Exception:
                pass
        db.delete(pack)

    # optional file cleanup
    if prediction.original_image_path and os.path.exists(prediction.original_image_path):
        try:
            os.remove(prediction.original_image_path)
        except Exception:
            pass

    if prediction.output_image_path and os.path.exists(prediction.output_image_path):
        try:
            os.remove(prediction.output_image_path)
        except Exception:
            pass

    db.delete(prediction)
    db.commit()

    return {"message": "Prediction deleted successfully"}


def set_active_workspace_prediction(db: Session, user_id: int, prediction_id: int) -> Prediction:
    db.query(Prediction).filter(Prediction.user_id == user_id).update(
        {Prediction.active_workspace: False},
        synchronize_session=False,
    )
    prediction = get_prediction_by_id(db, prediction_id, user_id)
    prediction.active_workspace = True
    db.commit()
    db.refresh(prediction)
    return prediction


def get_active_workspace_prediction(db: Session, user_id: int) -> Prediction | None:
    prediction = (
        db.query(Prediction)
        .filter(Prediction.user_id == user_id, Prediction.active_workspace == True)
        .order_by(Prediction.created_at.desc())
        .first()
    )
    if prediction:
        return prediction

    return (
        db.query(Prediction)
        .filter(Prediction.user_id == user_id)
        .order_by(
            Prediction.output_image_path.is_(None),
            Prediction.created_at.desc(),
        )
        .first()
    )
