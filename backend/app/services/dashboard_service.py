from __future__ import annotations

import os
import re
import shutil
from pathlib import Path

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.batch_job import BatchJob, BatchJobItem
from app.models.collection import CollectionItem
from app.models.delivery_pack import DeliveryPack
from app.models.edit_version import EditVersion
from app.models.prediction import Prediction
from app.models.share_link import ShareLink
from app.models.user import User
from app.services.prediction_service import get_active_workspace_prediction, get_prediction_by_id
from app.utils.filename_generator import infer_scene_label

TOOL_REGISTRY = [
    {"id": "remove_reflection", "title": "Remove Reflection", "category": "core", "description": "Clean glass glare and reflection artifacts."},
    {"id": "remove_glare", "title": "Remove Glare", "category": "core", "description": "Reduce harsh highlights and bright reflective spots."},
    {"id": "enhance_clarity", "title": "Enhance Clarity", "category": "core", "description": "Improve architectural sharpness and visibility."},
    {"id": "preserve_details", "title": "Preserve Details", "category": "core", "description": "Protect edges, facade lines, and textures."},
    {"id": "color_restore", "title": "Color Restore", "category": "core", "description": "Balance color shifts caused by glass reflections."},
    {"id": "before_after_poster", "title": "Before/After Poster", "category": "creative", "description": "Create comparison graphics."},
    {"id": "collage_maker", "title": "Collage Maker", "category": "creative", "description": "Generate client-ready layouts."},
    {"id": "client_showcase", "title": "Client Showcase", "category": "creative", "description": "Prepare presentation views."},
    {"id": "crop", "title": "Crop", "category": "utility", "description": "Crop the image."},
    {"id": "resize", "title": "Resize", "category": "utility", "description": "Resize output dimensions."},
    {"id": "format_converter", "title": "Format Converter", "category": "utility", "description": "Convert image formats."},
]

ALBUMS = {
    "glass-facades": {
        "name": "Glass Facades",
        "description": "Restored images with glass buildings, windows, and reflective facades.",
        "match": ["glass_facade", "glass-facade", "Glass Facade", "Glass Facades"],
    },
    "high-reflection": {
        "name": "High Reflection",
        "description": "Images containing strong glare or reflection interference.",
        "match": ["high_reflection", "high-reflection", "high_glare", "High Reflection", "High Glare"],
    },
    "interior-spaces": {
        "name": "Interior Spaces",
        "description": "Indoor architectural images with glass or reflective surfaces.",
        "match": ["interior", "interior_spaces", "Interior", "Interior Spaces"],
    },
    "outdoor-architecture": {
        "name": "Outdoor Architecture",
        "description": "Outdoor building, facade, and city architecture images.",
        "match": ["outdoor", "outdoor_architecture", "Outdoor", "Outdoor Architecture"],
    },
    "client-deliveries": {
        "name": "Client Deliveries",
        "description": "Completed results ready for sharing, preview, or export.",
        "match": ["client_delivery", "client-delivery", "Client Deliveries", "completed", "shared"],
    },
    "miscellaneous": {
        "name": "Miscellaneous",
        "description": "Results that do not clearly fit another category.",
        "match": ["misc", "miscellaneous", "Miscellaneous", None, ""],
    },
}


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _uploads_root() -> Path:
    return (_project_root() / "uploads").resolve()


def file_path_to_url(path: str | None) -> str | None:
    if not path:
        return None

    target = Path(path)
    if not target.is_absolute():
        target = (_project_root() / target).resolve()

    try:
        normalized = target.relative_to(_uploads_root()).as_posix()
    except ValueError:
        return None

    return f"/uploads/{normalized}"


def serialize_prediction(prediction: Prediction | None) -> dict | None:
    if not prediction:
        return None

    filename = prediction.original_filename or os.path.basename(prediction.original_image_path)
    stem = filename.rsplit(".", 1)[0]
    display_name = None if stem and len(stem) >= 20 and all(ch in "0123456789abcdefABCDEF" for ch in stem) else stem.replace("_", " ").replace("-", " ")

    return {
        "id": prediction.id,
        "filename": filename,
        "display_name": display_name,
        "original_url": file_path_to_url(prediction.original_image_path),
        "processed_url": file_path_to_url(prediction.output_image_path),
        "status": prediction.status,
        "category": prediction.category,
        "project_id": prediction.project_id,
        "width": prediction.width,
        "height": prediction.height,
        "source": prediction.source,
        "thumbnail_url": file_path_to_url(prediction.thumbnail_path) or file_path_to_url(prediction.output_image_path) or file_path_to_url(prediction.original_image_path),
        "download_url": file_path_to_url(prediction.output_image_path or prediction.original_image_path),
        "created_at": prediction.created_at.isoformat(),
        "updated_at": prediction.updated_at.isoformat() if prediction.updated_at else prediction.created_at.isoformat(),
    }


def serialize_user(user: User) -> dict:
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
    }


def _normalize_term(value: str | None) -> str:
    return (value or "").strip().lower()


def _slug_candidate(value: str | None) -> str:
    if value is None:
        return ""
    normalized = str(value).strip().lower()
    normalized = normalized.replace("_", "-").replace(" ", "-")
    normalized = re.sub(r"[^a-z0-9-]+", "", normalized)
    normalized = re.sub(r"-{2,}", "-", normalized).strip("-")
    return normalized


def normalize_category(value: str | None) -> str:
    if value is None or not str(value).strip():
        return "miscellaneous"

    normalized = _slug_candidate(value)

    if not normalized:
        return "miscellaneous"

    for slug, config in ALBUMS.items():
        candidates = [slug, *(config.get("match") or [])]
        normalized_candidates = {_slug_candidate(candidate) for candidate in candidates if candidate is not None}
        if normalized in normalized_candidates:
            return slug

    return normalized


def _extract_ml_metadata(db: Session, prediction_id: int) -> dict:
    version = (
        db.query(EditVersion)
        .filter(EditVersion.image_id == prediction_id, EditVersion.version_type == "processed")
        .order_by(EditVersion.created_at.desc())
        .first()
    )
    return version.ml_metadata or {} if version else {}


def _match_filename_category(filename: str) -> str | None:
    normalized_filename = _normalize_term(filename)
    if not normalized_filename:
        return None

    if any(term in normalized_filename for term in ("interior", "indoor", "lobby", "room", "hall")):
        return "interior-spaces"
    if any(term in normalized_filename for term in ("outdoor", "exterior", "street", "skyline", "city")):
        return "outdoor-architecture"
    if any(term in normalized_filename for term in ("glare", "reflection", "reflective", "mirror")):
        return "high-reflection"
    if any(term in normalized_filename for term in ("glass", "facade", "faade", "window", "building", "tower")):
        return "glass-facades"
    return None


def _infer_album_from_prediction(prediction: Prediction) -> str | None:
    original_filename = prediction.original_filename or ""
    stored_filename = prediction.stored_filename or os.path.basename(prediction.original_image_path or "")

    for candidate in (original_filename, stored_filename):
        matched = _match_filename_category(candidate)
        if matched:
            return matched

    scene_label = infer_scene_label(original_filename or stored_filename)
    scene_map = {
        "interior": "interior-spaces",
        "room": "interior-spaces",
        "lobby": "interior-spaces",
        "exterior": "outdoor-architecture",
        "architecture": "outdoor-architecture",
        "building": "outdoor-architecture",
        "office": "glass-facades",
        "storefront": "glass-facades",
        "facade": "glass-facades",
        "glass": "glass-facades",
        "window": "glass-facades",
    }
    mapped_scene = scene_map.get(scene_label)
    if mapped_scene:
        return mapped_scene

    if prediction.output_image_path or _normalize_term(prediction.status) == "completed":
        return "glass-facades"

    return None


def get_album_slug_for_prediction(
    prediction: Prediction,
    *,
    metadata: dict | None = None,
    shared_image_ids: set[int] | None = None,
) -> str:
    raw_category = getattr(prediction, "category", None)
    normalized_category = normalize_category(raw_category) if str(raw_category or "").strip() else None
    if normalized_category in ALBUMS:
        return normalized_category

    metadata_value = (metadata or {}).get("category")
    metadata_category = normalize_category(metadata_value) if str(metadata_value or "").strip() else None
    if metadata_category in ALBUMS:
        return metadata_category

    if shared_image_ids and prediction.id in shared_image_ids:
        return "client-deliveries"

    status = _normalize_term(prediction.status)
    if status in {"completed", "shared"} and shared_image_ids and prediction.id in shared_image_ids:
        return "client-deliveries"

    inferred_album = _infer_album_from_prediction(prediction)
    if inferred_album:
        return inferred_album

    return "miscellaneous"


def categorize_prediction(db: Session, prediction: Prediction) -> str:
    return get_album_slug_for_prediction(
        prediction,
        metadata=_extract_ml_metadata(db, prediction.id),
    )


def assign_prediction_category(db: Session, prediction: Prediction) -> str:
    shared_image_ids = {
        image_id
        for image_id, in db.query(ShareLink.image_id).filter(ShareLink.user_id == prediction.user_id).all()
    }
    category = get_album_slug_for_prediction(
        prediction,
        metadata=_extract_ml_metadata(db, prediction.id),
        shared_image_ids=shared_image_ids,
    )
    if prediction.category != category:
        prediction.category = category
        db.commit()
        db.refresh(prediction)
    return category


def get_filtered_tools(search: str | None) -> list[dict]:
    if not search:
        return TOOL_REGISTRY
    term = search.strip().lower()
    return [
        tool
        for tool in TOOL_REGISTRY
        if term in tool["title"].lower() or term in tool["description"].lower()
    ]


def _prediction_query(db: Session, user: User):
    return (
        db.query(Prediction)
        .filter(Prediction.user_id == user.id)
    )


def _ordered_predictions(query):
    return query.order_by(Prediction.updated_at.desc(), Prediction.created_at.desc(), Prediction.id.desc())


def _latest_predictions(query):
    return query.order_by(Prediction.created_at.desc(), Prediction.id.desc())


def _serialize_predictions(db: Session, predictions: list[Prediction]) -> list[dict]:
    items = []
    for prediction in predictions:
        assign_prediction_category(db, prediction)
        items.append(serialize_prediction(prediction))
    return items


def build_workspace_payload(db: Session, user: User) -> dict:
    latest_completed = (
        _latest_predictions(
            _prediction_query(db, user).filter(Prediction.status == "completed", Prediction.output_image_path.isnot(None))
        )
        .first()
    )
    latest_uploaded = _latest_predictions(_prediction_query(db, user)).first()
    latest = latest_completed or latest_uploaded

    latest_result = None
    if latest:
        assign_prediction_category(db, latest)
        latest_result = serialize_prediction(latest)

    total_processed = db.query(func.count(Prediction.id)).filter(Prediction.user_id == user.id, Prediction.status == "completed").scalar() or 0
    total_batches = db.query(func.count(BatchJob.id)).filter(BatchJob.user_id == user.id).scalar() or 0
    shared_links = db.query(func.count(ShareLink.id)).filter(ShareLink.user_id == user.id).scalar() or 0
    current_image = serialize_prediction(get_active_workspace_prediction(db, user.id))
    recent_predictions = _ordered_predictions(_prediction_query(db, user)).limit(4).all()
    recent_history = _serialize_predictions(db, recent_predictions)
    albums = get_smart_albums_payload(db, user)["albums"]

    return {
        "user": serialize_user(user),
        "latest_result": latest_result,
        "history": recent_history,
        "recent_history": recent_history,
        "smart_albums": albums,
        "albums": albums,
        "stats": {
            "total_processed": total_processed,
            "total_batches": total_batches,
            "shared_links": shared_links,
        },
        "current_image": current_image or latest_result,
        "workspace": {"current_image": current_image or latest_result},
    }


def get_dashboard_result_payload(db: Session, user: User, image_id: int) -> dict:
    prediction = get_prediction_by_id(db, image_id, user.id)
    assign_prediction_category(db, prediction)
    item = serialize_prediction(prediction)
    return {"item": item}


def get_history_payload(
    db: Session,
    user: User,
    *,
    limit: int | None = None,
    offset: int = 0,
    status: str | None = None,
    search: str | None = None,
) -> dict:
    query = _prediction_query(db, user)

    if status and status.lower() != "all":
        query = query.filter(Prediction.status == status.lower())

    if search:
        term = f"%{search.strip()}%"
        query = query.filter(
            Prediction.original_filename.ilike(term) | Prediction.stored_filename.ilike(term)
        )

    total = query.count()
    query = _ordered_predictions(query).offset(max(offset, 0))
    if limit is not None:
        query = query.limit(max(1, min(limit, 100)))

    predictions = query.all()
    return {"items": _serialize_predictions(db, predictions), "total": total}


def delete_history_item(db: Session, user: User, image_id: int) -> dict:
    prediction = get_prediction_by_id(db, image_id, user.id)

    db.query(ShareLink).filter(ShareLink.image_id == prediction.id, ShareLink.user_id == user.id).delete(synchronize_session=False)
    db.query(EditVersion).filter(EditVersion.image_id == prediction.id, EditVersion.user_id == user.id).delete(synchronize_session=False)
    db.query(CollectionItem).filter(CollectionItem.prediction_id == prediction.id).delete(synchronize_session=False)

    delivery_packs = db.query(DeliveryPack).filter(DeliveryPack.prediction_id == prediction.id, DeliveryPack.user_id == user.id).all()
    for pack in delivery_packs:
        if pack.file_path and os.path.exists(pack.file_path):
            try:
                os.remove(pack.file_path)
            except OSError:
                pass
        db.delete(pack)

    batch_items = db.query(BatchJobItem).filter(BatchJobItem.image_id == prediction.id).all()
    batch_ids = {item.batch_job_id for item in batch_items}
    for item in batch_items:
        db.delete(item)
    db.flush()

    for batch_id in batch_ids:
        batch = db.query(BatchJob).filter(BatchJob.id == batch_id, BatchJob.user_id == user.id).first()
        if batch:
            remaining_items = db.query(BatchJobItem).filter(BatchJobItem.batch_job_id == batch.id).count()
            if remaining_items == 0:
                if batch.zip_path and os.path.exists(batch.zip_path):
                    try:
                        os.remove(batch.zip_path)
                    except OSError:
                        pass
                db.delete(batch)
            else:
                batch.total_count = remaining_items
                batch.completed_count = (
                    db.query(func.count(BatchJobItem.id))
                    .filter(BatchJobItem.batch_job_id == batch.id, BatchJobItem.status == "completed")
                    .scalar()
                    or 0
                )
                batch.failed_count = (
                    db.query(func.count(BatchJobItem.id))
                    .filter(BatchJobItem.batch_job_id == batch.id, BatchJobItem.status == "failed")
                    .scalar()
                    or 0
                )

    for path in {prediction.original_image_path, prediction.output_image_path, prediction.thumbnail_path}:
        if path and os.path.exists(path):
            try:
                os.remove(path)
            except OSError:
                pass

    db.delete(prediction)
    db.commit()
    return {"message": "History item deleted successfully"}


def _group_album_predictions(db: Session, user: User) -> dict[str, list[dict]]:
    predictions = _ordered_predictions(_prediction_query(db, user)).all()
    shared_image_ids = {
        image_id
        for image_id, in db.query(ShareLink.image_id).filter(ShareLink.user_id == user.id).all()
    }
    metadata_by_prediction_id: dict[int, dict] = {}
    for version in (
        db.query(EditVersion)
        .filter(EditVersion.user_id == user.id, EditVersion.version_type == "processed")
        .order_by(EditVersion.image_id.asc(), EditVersion.created_at.desc())
        .all()
    ):
        metadata_by_prediction_id.setdefault(version.image_id, version.ml_metadata or {})

    grouped: dict[str, list[dict]] = {slug: [] for slug in ALBUMS}
    for prediction in predictions:
        slug = get_album_slug_for_prediction(
            prediction,
            metadata=metadata_by_prediction_id.get(prediction.id),
            shared_image_ids=shared_image_ids,
        )
        if prediction.category != slug:
            prediction.category = slug
        item = serialize_prediction(prediction)
        if item:
            grouped.setdefault(slug if slug in ALBUMS else "miscellaneous", []).append(item)
    db.commit()
    return grouped


def get_smart_albums_payload(db: Session, user: User) -> dict:
    grouped = _group_album_predictions(db, user)
    albums = []

    for slug, config in ALBUMS.items():
        items = grouped.get(slug, [])
        cover_source = next((item for item in items if item.get("processed_url") or item.get("original_url")), None)
        albums.append(
            {
                "slug": slug,
                "name": config["name"],
                "description": config["description"],
                "count": len(items),
                "cover_url": (cover_source or {}).get("processed_url") or (cover_source or {}).get("original_url"),
                "updated_at": items[0]["created_at"] if items else None,
            }
        )

    return {"albums": albums}


def get_album_detail_payload(db: Session, user: User, album_slug: str) -> dict:
    normalized_slug = normalize_category(album_slug)
    if normalized_slug not in ALBUMS:
        raise HTTPException(status_code=404, detail="Album not found")

    grouped = _group_album_predictions(db, user)
    items = grouped.get(normalized_slug, [])
    config = ALBUMS[normalized_slug]
    return {
        "slug": normalized_slug,
        "name": config["name"],
        "description": config["description"],
        "updated_at": items[0]["created_at"] if items else None,
        "count": len(items),
        "items": items,
    }


def get_demo_asset_paths() -> tuple[str, str]:
    project_root = _project_root().parent
    source_dir = project_root / "reflection-removal-frontend" / "src" / "lib" / "assets"
    uploads_demo = _uploads_root() / "demo"
    uploads_demo.mkdir(parents=True, exist_ok=True)

    original_target = uploads_demo / "demo_original.jpg"
    processed_target = uploads_demo / "demo_processed.jpg"

    if not original_target.exists():
        shutil.copy2(source_dir / "input.jpg", original_target)
    if not processed_target.exists():
        shutil.copy2(source_dir / "output.jpg", processed_target)

    return str(original_target), str(processed_target)
