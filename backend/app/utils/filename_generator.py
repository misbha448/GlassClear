import os
import re
from datetime import datetime
from pathlib import Path


DEFAULT_SCENE = "scene"
SCENE_KEYWORDS = (
    "window",
    "indoor",
    "architecture",
    "architectural",
    "building",
    "office",
    "interior",
    "exterior",
    "storefront",
    "retail",
    "product",
    "hotel",
    "lobby",
    "facade",
    "glass",
    "room",
)


def _slugify(value: str) -> str:
    cleaned = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    return cleaned or DEFAULT_SCENE


def normalize_mode(mode: str | None) -> str:
    value = (mode or "").strip().lower()
    if value in {"quality", "enhanced", "hd"}:
        return "enhanced"
    if value in {"clean", "fidelity", "standard"}:
        return "clean"
    return "clean"


def normalize_extension(target_format: str | None, fallback_filename: str | None = None) -> str:
    if target_format:
        ext = target_format.strip().lower().lstrip(".")
    else:
        ext = Path(fallback_filename or "").suffix.lower().lstrip(".")

    if ext in {"jpg", "jpeg"}:
        return "jpg"
    if ext in {"png", "webp"}:
        return ext
    return "png"


def infer_scene_label(original_filename: str | None) -> str:
    stem = Path(original_filename or "").stem
    slug = _slugify(stem)

    for keyword in SCENE_KEYWORDS:
        if keyword in slug:
            return "architecture" if keyword == "architectural" else keyword

    parts = [
        part
        for part in slug.split("_")
        if part and part not in {"img", "image", "photo", "glassclear"}
    ]
    return "_".join(parts[:2]) if parts else DEFAULT_SCENE


def generate_filename(
    mode: str,
    original_filename: str | None,
    target_format: str,
    output_dir: str,
    scene: str | None = None,
) -> str:
    normalized_mode = normalize_mode(mode)
    normalized_scene = _slugify(scene or infer_scene_label(original_filename))
    normalized_ext = normalize_extension(target_format, original_filename)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    base_name = f"GC_{normalized_mode}_{normalized_scene}_{timestamp}"
    candidate = f"{base_name}.{normalized_ext}"
    counter = 1

    while os.path.exists(os.path.join(output_dir, candidate)):
        candidate = f"{base_name}_{counter}.{normalized_ext}"
        counter += 1

    return candidate
