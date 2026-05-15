from __future__ import annotations

import mimetypes
import os
import re
import uuid
from pathlib import Path

from fastapi import HTTPException
from PIL import Image, ImageDraw

from app.models.prediction import Prediction


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _uploads_root() -> Path:
    return (_project_root() / "uploads").resolve()


def _exports_root() -> Path:
    exports_root = (_uploads_root() / "exports").resolve()
    exports_root.mkdir(parents=True, exist_ok=True)
    return exports_root


def _display_title(prediction: Prediction) -> str:
    raw_name = prediction.original_filename or os.path.basename(prediction.original_image_path or "")
    stem = Path(raw_name).stem
    if stem and len(stem) >= 20 and all(ch in "0123456789abcdefABCDEF" for ch in stem):
        return "GlassClear Restoration"
    clean = re.sub(r"[_-]+", " ", stem).strip()
    return clean or "GlassClear Result"


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    return slug or "glassclear_result"


def _ensure_prediction_files(prediction: Prediction) -> tuple[Path, Path]:
    original_path = Path(prediction.original_image_path or "")
    processed_path = Path(prediction.output_image_path or "")

    if not original_path.exists():
        raise HTTPException(status_code=404, detail="Original image file not found.")
    if not processed_path.exists():
        raise HTTPException(status_code=404, detail="Processed image file not found.")

    return original_path, processed_path


def create_comparison_export(prediction: Prediction, title: str | None = None) -> tuple[str, str]:
    original_path, processed_path = _ensure_prediction_files(prediction)

    with Image.open(original_path).convert("RGB") as original_image, Image.open(processed_path).convert("RGB") as processed_image:
        panel_width = 1360
        panel_height = 880
        canvas = Image.new("RGB", (panel_width * 2 + 120, panel_height + 190), "#f7f8fc")
        draw = ImageDraw.Draw(canvas)

        def fit_panel(image: Image.Image) -> Image.Image:
            fitted = image.copy()
            fitted.thumbnail((panel_width, panel_height))
            frame = Image.new("RGB", (panel_width, panel_height), "#ffffff")
            offset_x = (panel_width - fitted.width) // 2
            offset_y = (panel_height - fitted.height) // 2
            frame.paste(fitted, (offset_x, offset_y))
            return frame

        before_panel = fit_panel(original_image)
        after_panel = fit_panel(processed_image)

        canvas.paste(before_panel, (40, 130))
        canvas.paste(after_panel, (panel_width + 80, 130))

        heading = title or _display_title(prediction)
        draw.text((40, 34), f"GlassClear Comparison | {heading}", fill="#18253c")
        draw.text((40, 88), "Original", fill="#5f6b85")
        draw.text((panel_width + 80, 88), "GlassClear Output", fill="#5f6b85")
        draw.rounded_rectangle((32, 122, panel_width + 48, panel_height + 138), radius=28, outline="#d9dfed", width=2)
        draw.rounded_rectangle((panel_width + 72, 122, panel_width * 2 + 88, panel_height + 138), radius=28, outline="#d9dfed", width=2)
        draw.text((40, panel_height + 152), "Automated Glare & Reflection Elimination", fill="#7b859d")

        base_name = _slugify(heading)
        output_path = _exports_root() / f"{base_name}_comparison_{uuid.uuid4().hex}.jpg"
        canvas.save(output_path, "JPEG", quality=97, optimize=True)

    return str(output_path), f"GlassClear_{base_name}_comparison.jpg"


def create_export_asset(prediction: Prediction, export_format: str) -> tuple[str, str, str]:
    _, processed_path = _ensure_prediction_files(prediction)
    export_format = (export_format or "png").lower()
    title = _display_title(prediction)
    base_name = _slugify(title)

    if export_format == "comparison":
        path, filename = create_comparison_export(prediction, title)
        media_type = mimetypes.guess_type(path)[0] or "image/jpeg"
        return path, filename, media_type

    if export_format == "hd":
        extension = processed_path.suffix.lower() or ".png"
        filename = f"GlassClear_{base_name}_hd{extension}"
        media_type = mimetypes.guess_type(str(processed_path))[0] or "application/octet-stream"
        return str(processed_path), filename, media_type

    if export_format not in {"jpg", "png"}:
        raise HTTPException(status_code=400, detail="Unsupported export format.")

    with Image.open(processed_path).convert("RGB") as processed_image:
        extension = ".jpg" if export_format == "jpg" else ".png"
        output_path = _exports_root() / f"{base_name}_{export_format}_{uuid.uuid4().hex}{extension}"
        if export_format == "jpg":
            processed_image.save(output_path, "JPEG", quality=97, optimize=True)
        else:
            processed_image.save(output_path, "PNG", compress_level=0)

    filename = f"GlassClear_{base_name}{extension}"
    media_type = mimetypes.guess_type(str(output_path))[0] or "application/octet-stream"
    return str(output_path), filename, media_type
