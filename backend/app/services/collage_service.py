from __future__ import annotations

import os
import uuid
from pathlib import Path
from urllib.parse import urlparse

from fastapi import HTTPException
from PIL import Image, ImageDraw
from sqlalchemy.orm import Session

from app.models.collage_asset import CollageAsset
from app.models.user import User
from app.schemas.collage import CollageImageInput
from app.services.dashboard_service import file_path_to_url
from app.services.prediction_service import get_prediction_by_id

UPLOADS_ROOT = (Path(__file__).resolve().parents[2] / "uploads").resolve()
COLLAGE_ROOT = (UPLOADS_ROOT / "collages").resolve()
CANVAS_BG = "#f6f8fd"
TEXT_COLOR = "#1b2740"
ACCENT_COLOR = "#2f6cff"


def _resolve_upload_path(url: str) -> str:
    parsed = urlparse(url)
    path = parsed.path or url
    if not path.startswith("/uploads/"):
        raise HTTPException(status_code=400, detail="Only uploaded workspace images can be used for collages")

    relative_path = path.removeprefix("/uploads/")
    target = (UPLOADS_ROOT / relative_path).resolve()
    if not str(target).startswith(str(UPLOADS_ROOT)) or not target.exists():
        raise HTTPException(status_code=404, detail="Selected collage image was not found")
    return str(target)


def _fit_size(image: Image.Image, width: int, height: int) -> Image.Image:
    return image.resize((width, height))


def _draw_label(draw: ImageDraw.ImageDraw, x: int, y: int, text: str) -> None:
    draw.rounded_rectangle((x, y, x + 210, y + 34), radius=12, fill=(255, 255, 255))
    draw.text((x + 12, y + 9), text, fill=TEXT_COLOR)


def _draw_cover(canvas: Image.Image, image: Image.Image, box: tuple[int, int, int, int]) -> None:
    x, y, width, height = box
    fitted = image.copy()
    fitted.thumbnail((width, height))
    frame = Image.new("RGB", (width, height), "#e4ebf5")
    frame.paste(fitted, ((width - fitted.width) // 2, (height - fitted.height) // 2))
    canvas.paste(frame, (x, y))


def _normalize_sources(
    db: Session,
    user: User,
    image_ids: list[int] | None,
    images: list[CollageImageInput] | None,
) -> tuple[list[dict], list[int | str]]:
    normalized_sources: list[dict] = []
    stored_ids: list[int | str] = []

    for image_id in image_ids or []:
        prediction = get_prediction_by_id(db, image_id, user.id)
        if prediction.output_image_path and os.path.exists(prediction.output_image_path):
            normalized_sources.append(
                {
                    "path": prediction.output_image_path,
                    "label": prediction.original_filename or "GlassClear Output",
                    "prediction_id": prediction.id,
                    "project_id": prediction.project_id,
                }
            )
            stored_ids.append(prediction.id)

    for image in images or []:
        if image.image_id is not None:
            prediction = get_prediction_by_id(db, image.image_id, user.id)
            source_path = prediction.output_image_path or prediction.original_image_path
            normalized_sources.append(
                {
                    "path": source_path,
                    "label": image.label or prediction.original_filename or "Workspace Image",
                    "prediction_id": prediction.id,
                    "project_id": prediction.project_id,
                }
            )
            stored_ids.append(prediction.id)
            continue

        if image.url:
            normalized_sources.append(
                {
                    "path": _resolve_upload_path(image.url),
                    "label": image.label or "Workspace Image",
                    "prediction_id": None,
                    "project_id": None,
                }
            )
            stored_ids.append(image.url)

    if not normalized_sources:
        raise HTTPException(status_code=400, detail="No images available for collage generation")

    return normalized_sources, stored_ids


def _open_image(path: str) -> Image.Image:
    return Image.open(path).convert("RGB")


def _build_collage(layout_type: str, title: str, sources: list[dict]) -> str:
    COLLAGE_ROOT.mkdir(parents=True, exist_ok=True)
    output_path = str(COLLAGE_ROOT / f"{layout_type}_{uuid.uuid4().hex}.png")

    if layout_type == "before_after_split":
        if len(sources) < 2:
            raise HTTPException(status_code=400, detail="Before/After Split requires two images")
        images = [_fit_size(_open_image(item["path"]), 900, 620) for item in sources[:2]]
        canvas = Image.new("RGB", (1840, 760), CANVAS_BG)
        canvas.paste(images[0], (20, 120))
        canvas.paste(images[1], (920, 120))
        draw = ImageDraw.Draw(canvas)
        draw.text((28, 30), title, fill=TEXT_COLOR)
        _draw_label(draw, 40, 70, sources[0]["label"] or "Original")
        _draw_label(draw, 940, 70, sources[1]["label"] or "GlassClear Output")
    elif layout_type == "two_image_board":
        if len(sources) < 2:
            raise HTTPException(status_code=400, detail="2 Image Board requires two images")
        canvas = Image.new("RGB", (1840, 760), CANVAS_BG)
        draw = ImageDraw.Draw(canvas)
        draw.text((28, 30), title, fill=TEXT_COLOR)
        positions = [(20, 120, 880, 600), (940, 120, 880, 600)]
        for source, box in zip(sources[:2], positions):
            _draw_cover(canvas, _open_image(source["path"]), box)
            _draw_label(draw, box[0], 70, source["label"] or "Workspace Image")
    elif layout_type == "four_image_showcase":
        if len(sources) < 2:
            raise HTTPException(status_code=400, detail="4 Image Showcase requires at least two images")
        canvas = Image.new("RGB", (1840, 1240), CANVAS_BG)
        draw = ImageDraw.Draw(canvas)
        draw.text((28, 30), title, fill=TEXT_COLOR)
        positions = [
            (20, 120, 880, 500),
            (940, 120, 880, 500),
            (20, 650, 880, 500),
            (940, 650, 880, 500),
        ]
        for source, box in zip(sources[:4], positions):
            _draw_cover(canvas, _open_image(source["path"]), box)
            _draw_label(draw, box[0], box[1] - 40, source["label"] or "Workspace Image")
    elif layout_type == "client_comparison_poster":
        if len(sources) < 2:
            raise HTTPException(status_code=400, detail="Client Comparison Poster requires two images")
        canvas = Image.new("RGB", (1200, 1560), CANVAS_BG)
        draw = ImageDraw.Draw(canvas)
        draw.text((60, 40), title, fill=TEXT_COLOR)
        draw.text((60, 92), "GlassClear", fill=ACCENT_COLOR)
        boxes = [(60, 180, 1080, 560), (60, 850, 1080, 560)]
        for source, box in zip(sources[:2], boxes):
            _draw_cover(canvas, _open_image(source["path"]), box)
            _draw_label(draw, box[0], box[1] - 44, source["label"] or "Workspace Image")
    elif layout_type == "project_contact_sheet":
        if len(sources) < 3:
            raise HTTPException(status_code=400, detail="Project Contact Sheet requires at least three images")
        canvas = Image.new("RGB", (1840, 1560), CANVAS_BG)
        draw = ImageDraw.Draw(canvas)
        draw.text((28, 30), title, fill=TEXT_COLOR)
        positions = [
            (20, 120, 580, 400),
            (630, 120, 580, 400),
            (1240, 120, 580, 400),
            (20, 560, 580, 400),
            (630, 560, 580, 400),
            (1240, 560, 580, 400),
        ]
        for source, box in zip(sources[:6], positions):
            _draw_cover(canvas, _open_image(source["path"]), box)
            _draw_label(draw, box[0], box[1] - 40, source["label"] or "Workspace Image")
    elif layout_type == "social_preview":
        if len(sources) < 2:
            raise HTTPException(status_code=400, detail="Social Preview requires at least two images")
        canvas = Image.new("RGB", (1080, 1080), CANVAS_BG)
        draw = ImageDraw.Draw(canvas)
        draw.text((44, 36), title, fill=TEXT_COLOR)
        draw.text((44, 84), "Automated reflection and glare cleanup", fill=ACCENT_COLOR)
        positions = [(44, 160, 480, 780), (556, 160, 480, 780)]
        for source, box in zip(sources[:2], positions):
            _draw_cover(canvas, _open_image(source["path"]), box)
            _draw_label(draw, box[0], 124, source["label"] or "Workspace Image")
    else:
        raise HTTPException(status_code=400, detail="Unsupported collage layout")

    canvas.save(output_path, "PNG")
    return output_path


def create_collage(
    db: Session,
    user: User,
    layout_type: str,
    title: str,
    image_ids: list[int] | None = None,
    images: list[CollageImageInput] | None = None,
) -> dict:
    sources, stored_ids = _normalize_sources(db, user, image_ids, images)
    output_path = _build_collage(layout_type, title, sources)
    project_id = next((source["project_id"] for source in sources if source["project_id"]), None)

    collage = CollageAsset(
        user_id=user.id,
        project_id=project_id,
        title=title,
        layout_type=layout_type,
        image_ids=stored_ids,
        output_path=output_path,
        status="generated",
    )
    db.add(collage)
    db.commit()
    db.refresh(collage)
    return {
        "success": True,
        "output_url": file_path_to_url(collage.output_path),
        "collage": {
            "id": collage.id,
            "title": collage.title,
            "layout_type": collage.layout_type,
            "output_url": file_path_to_url(collage.output_path),
            "created_at": collage.created_at.isoformat(),
        },
    }


def list_collages(db: Session, user: User) -> dict:
    collages = db.query(CollageAsset).filter(CollageAsset.user_id == user.id).order_by(CollageAsset.created_at.desc()).all()
    return {
        "collages": [
            {
                "id": collage.id,
                "title": collage.title,
                "layout_type": collage.layout_type,
                "output_url": file_path_to_url(collage.output_path),
                "status": collage.status,
                "created_at": collage.created_at.isoformat(),
            }
            for collage in collages
        ]
    }


def delete_collage(db: Session, user: User, collage_id: int) -> dict:
    collage = db.query(CollageAsset).filter(CollageAsset.id == collage_id, CollageAsset.user_id == user.id).first()
    if not collage:
        raise HTTPException(status_code=404, detail="Collage not found")
    if collage.output_path and os.path.exists(collage.output_path):
        os.remove(collage.output_path)
    db.delete(collage)
    db.commit()
    return {"message": "Collage deleted"}
