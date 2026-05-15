from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.collection import Collection, CollectionItem
from app.models.prediction import Prediction
from app.models.user import User
from app.services.dashboard_service import file_path_to_url, serialize_prediction
from app.services.prediction_service import get_prediction_by_id


def _collection_query(db: Session, user_id: int):
    return db.query(Collection).filter(Collection.user_id == user_id)


def _serialize_collection_row(row: Collection, count: int = 0, cover_url: str | None = None, updated_at=None) -> dict:
    return {
        "id": row.id,
        "name": row.name,
        "count": int(count or 0),
        "cover_url": cover_url,
        "created_at": row.created_at.isoformat() if row.created_at else None,
        "updated_at": (updated_at or row.updated_at).isoformat() if (updated_at or row.updated_at) else None,
    }


def list_collections_payload(db: Session, user: User) -> dict:
    collections = _collection_query(db, user.id).order_by(Collection.updated_at.desc(), Collection.id.desc()).all()
    collection_ids = [collection.id for collection in collections]
    counts_by_collection: dict[int, int] = {}
    latest_prediction_by_collection: dict[int, Prediction] = {}

    if collection_ids:
        count_rows = (
            db.query(CollectionItem.collection_id, func.count(CollectionItem.id))
            .filter(CollectionItem.collection_id.in_(collection_ids))
            .group_by(CollectionItem.collection_id)
            .all()
        )
        counts_by_collection = {collection_id: count for collection_id, count in count_rows}

        latest_items = (
            db.query(CollectionItem)
            .filter(CollectionItem.collection_id.in_(collection_ids))
            .order_by(CollectionItem.collection_id.asc(), CollectionItem.created_at.desc(), CollectionItem.id.desc())
            .all()
        )
        latest_prediction_ids: dict[int, int] = {}
        for item in latest_items:
            latest_prediction_ids.setdefault(item.collection_id, item.prediction_id)

        if latest_prediction_ids:
            predictions = (
                db.query(Prediction)
                .filter(Prediction.id.in_(latest_prediction_ids.values()), Prediction.user_id == user.id)
                .all()
            )
            predictions_by_id = {prediction.id: prediction for prediction in predictions}
            latest_prediction_by_collection = {
                collection_id: predictions_by_id[prediction_id]
                for collection_id, prediction_id in latest_prediction_ids.items()
                if prediction_id in predictions_by_id
            }

    payload = []
    for collection in collections:
        prediction = latest_prediction_by_collection.get(collection.id)
        cover_url = None
        updated_at = collection.updated_at
        if prediction:
            cover_url = (
                file_path_to_url(prediction.thumbnail_path)
                or file_path_to_url(prediction.output_image_path)
                or file_path_to_url(prediction.original_image_path)
            )
            updated_at = prediction.updated_at or prediction.created_at

        payload.append(
            _serialize_collection_row(
                collection,
                count=counts_by_collection.get(collection.id, 0),
                cover_url=cover_url,
                updated_at=updated_at,
            )
        )

    return {"collections": payload}


def create_collection_payload(db: Session, user: User, name: str) -> dict:
    clean_name = (name or "").strip()
    if not clean_name:
        raise HTTPException(status_code=400, detail="Collection name is required.")

    collection = Collection(user_id=user.id, name=clean_name)
    db.add(collection)
    db.commit()
    db.refresh(collection)
    return _serialize_collection_row(collection)


def get_collection_or_404(db: Session, user_id: int, collection_id: int) -> Collection:
    collection = _collection_query(db, user_id).filter(Collection.id == collection_id).first()
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection


def add_collection_item_payload(db: Session, user: User, collection_id: int, prediction_id: int) -> dict:
    collection = get_collection_or_404(db, user.id, collection_id)
    prediction = get_prediction_by_id(db, prediction_id, user.id)

    existing = (
        db.query(CollectionItem)
        .filter(CollectionItem.collection_id == collection.id, CollectionItem.prediction_id == prediction.id)
        .first()
    )
    if existing:
        return {"message": "Item already exists in collection", "collection_id": collection.id, "prediction_id": prediction.id}

    item = CollectionItem(collection_id=collection.id, prediction_id=prediction.id)
    db.add(item)
    collection.updated_at = prediction.updated_at or prediction.created_at
    db.commit()
    return {"message": "Item added to collection", "collection_id": collection.id, "prediction_id": prediction.id}


def get_collection_detail_payload(db: Session, user: User, collection_id: int) -> dict:
    collection = get_collection_or_404(db, user.id, collection_id)
    items = (
        db.query(Prediction)
        .join(CollectionItem, CollectionItem.prediction_id == Prediction.id)
        .filter(CollectionItem.collection_id == collection.id, Prediction.user_id == user.id)
        .order_by(CollectionItem.created_at.desc(), CollectionItem.id.desc())
        .all()
    )
    serialized_items = []
    for prediction in items:
        item = serialize_prediction(prediction)
        if item:
            serialized_items.append(item)
    cover_url = serialized_items[0]["thumbnail_url"] if serialized_items else None
    updated_at = serialized_items[0]["updated_at"] if serialized_items else (collection.updated_at.isoformat() if collection.updated_at else None)

    return {
        "id": collection.id,
        "name": collection.name,
        "count": len(serialized_items),
        "cover_url": cover_url,
        "updated_at": updated_at,
        "items": serialized_items,
    }


def remove_collection_item_payload(db: Session, user: User, collection_id: int, prediction_id: int) -> dict:
    collection = get_collection_or_404(db, user.id, collection_id)
    item = (
        db.query(CollectionItem)
        .filter(CollectionItem.collection_id == collection.id, CollectionItem.prediction_id == prediction_id)
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Collection item not found")

    db.delete(item)
    db.commit()
    return {"message": "Item removed from collection"}
