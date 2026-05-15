from __future__ import annotations

import os
import uuid

try:
    from PIL import Image, ImageEnhance, ImageFilter
except ImportError:  # pragma: no cover
    Image = None
    ImageEnhance = None
    ImageFilter = None


def create_variation_images(source_path: str, output_dir: str = "uploads") -> list[dict[str, str]]:
    if Image is None or ImageEnhance is None or ImageFilter is None:
        raise RuntimeError("Pillow is required for AI variations")

    if not source_path or not os.path.exists(source_path):
        raise FileNotFoundError("Processed image not found")

    os.makedirs(output_dir, exist_ok=True)

    extension = os.path.splitext(source_path)[1] or ".png"
    variations_config = [
        {"key": "balanced", "label": "Balanced"},
        {"key": "aggressive_clean", "label": "Aggressive Clean"},
        {"key": "detail_preserve", "label": "Detail Preserve"},
    ]

    generated: list[dict[str, str]] = []

    with Image.open(source_path) as image:
        base = image.convert("RGB") if image.mode not in ("RGB", "RGBA") else image.copy()

        for variation in variations_config:
            working = base.copy()
            key = variation["key"]

            if key == "balanced":
                working = ImageEnhance.Contrast(working).enhance(1.05)
                working = ImageEnhance.Color(working).enhance(1.02)
                working = working.filter(ImageFilter.UnsharpMask(radius=1.2, percent=110, threshold=2))
            elif key == "aggressive_clean":
                working = ImageEnhance.Contrast(working).enhance(1.12)
                working = ImageEnhance.Color(working).enhance(0.98)
                working = working.filter(ImageFilter.UnsharpMask(radius=1.7, percent=145, threshold=2))
                working = ImageEnhance.Sharpness(working).enhance(1.12)
            elif key == "detail_preserve":
                working = ImageEnhance.Contrast(working).enhance(1.03)
                working = ImageEnhance.Color(working).enhance(1.03)
                working = working.filter(ImageFilter.UnsharpMask(radius=0.9, percent=90, threshold=1))
                working = ImageEnhance.Sharpness(working).enhance(1.18)

            filename = f"{key}_{uuid.uuid4().hex}{extension}"
            path = os.path.join(output_dir, filename)
            save_kwargs = {"quality": 96} if extension.lower() in {".jpg", ".jpeg"} else {}
            working.save(path, **save_kwargs)

            generated.append({
                "key": key,
                "label": variation["label"],
                "path": path
            })

    return generated
