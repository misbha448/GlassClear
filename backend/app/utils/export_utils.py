import os

import cv2
import numpy as np
from fastapi import HTTPException


IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}


def ensure_bgr_uint8(image: np.ndarray) -> np.ndarray:
    if image is None:
        raise HTTPException(status_code=500, detail="No image data available for export.")

    if not isinstance(image, np.ndarray):
        raise HTTPException(status_code=500, detail="Invalid image type for export.")

    array = image
    if array.dtype != np.uint8:
        array = np.clip(array, 0, 255).astype(np.uint8)

    if array.ndim == 2:
        return cv2.cvtColor(array, cv2.COLOR_GRAY2BGR)

    if array.ndim != 3:
        raise HTTPException(status_code=500, detail="Unsupported image shape for export.")

    channels = array.shape[2]
    if channels == 3:
        return array
    if channels == 4:
        return cv2.cvtColor(array, cv2.COLOR_BGRA2BGR)

    raise HTTPException(status_code=500, detail="Unsupported channel count for export.")


def get_extension(path: str) -> str:
    return os.path.splitext(path)[1].lower().lstrip(".")


def get_imwrite_params(extension: str) -> list[int]:
    if extension in {"jpg", "jpeg"}:
        return [cv2.IMWRITE_JPEG_QUALITY, 98]
    if extension == "png":
        return [cv2.IMWRITE_PNG_COMPRESSION, 0]
    if extension == "webp":
        return [cv2.IMWRITE_WEBP_QUALITY, 95]
    return []


def save_image_for_export(image: np.ndarray, output_path: str) -> str:
    extension = get_extension(output_path)
    if extension not in IMAGE_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Unsupported export format: {extension}")

    export_image = ensure_bgr_uint8(image)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    success = cv2.imwrite(output_path, export_image, get_imwrite_params(extension))
    if not success or not os.path.exists(output_path):
        raise HTTPException(status_code=500, detail="Failed to save processed image.")

    return output_path
