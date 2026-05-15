from __future__ import annotations

import os
import uuid

try:
    from PIL import Image, ImageEnhance, ImageFilter
except ImportError:  # pragma: no cover
    Image = None
    ImageEnhance = None
    ImageFilter = None


def create_enhanced_image(source_path: str, output_dir: str = "uploads") -> str:
    if Image is None or ImageEnhance is None or ImageFilter is None:
        raise RuntimeError("Pillow is required for AI enhancement")

    if not source_path or not os.path.exists(source_path):
        raise FileNotFoundError("Processed image not found")

    os.makedirs(output_dir, exist_ok=True)

    extension = os.path.splitext(source_path)[1] or ".png"
    enhanced_name = f"enhanced_{uuid.uuid4().hex}{extension}"
    enhanced_path = os.path.join(output_dir, enhanced_name)

    with Image.open(source_path) as image:
        working = image.convert("RGB") if image.mode not in ("RGB", "RGBA") else image.copy()
        working = working.filter(ImageFilter.UnsharpMask(radius=1.8, percent=135, threshold=2))
        working = ImageEnhance.Contrast(working).enhance(1.1)
        working = ImageEnhance.Color(working).enhance(1.04)
        working = ImageEnhance.Sharpness(working).enhance(1.08)

        save_kwargs = {"quality": 96} if extension.lower() in {".jpg", ".jpeg"} else {}
        working.save(enhanced_path, **save_kwargs)

    return enhanced_path
