import cv2
import numpy as np
from fastapi import HTTPException

from app.utils.export_utils import save_image_for_export
from app.utils.super_resolution import upscale_image

def _normalize_image(image: np.ndarray) -> np.ndarray:
    return cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX)


def _boost_contrast(image: np.ndarray) -> np.ndarray:
    return cv2.convertScaleAbs(image, alpha=1.12, beta=2)


def _soft_sharpen(image: np.ndarray) -> np.ndarray:
    blurred = cv2.GaussianBlur(image, (0, 0), 0.9)
    return cv2.addWeighted(image, 1.14, blurred, -0.14, 0)


def _increase_saturation(image: np.ndarray) -> np.ndarray:
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.08, 0, 255)
    return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)


def _light_denoise(image: np.ndarray) -> np.ndarray:
    return cv2.fastNlMeansDenoisingColored(image, None, 2, 2, 5, 13)


def _enhance_image_array(image: np.ndarray) -> np.ndarray:
    enhanced = _normalize_image(image)
    enhanced = _boost_contrast(enhanced)
    enhanced = _soft_sharpen(enhanced)
    enhanced = _increase_saturation(enhanced)
    return _light_denoise(enhanced)


def enhance_image(image_path: str, output_path: str) -> str:
    try:
        image = cv2.imread(image_path, cv2.IMREAD_COLOR)
        if image is None:
            raise HTTPException(status_code=400, detail="Unable to read processed image for enhancement.")

        enhanced = _enhance_image_array(image)
        enhanced = upscale_image(enhanced)

        return save_image_for_export(enhanced, output_path)
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Enhancement failed: {str(e)}")
