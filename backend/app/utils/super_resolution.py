from pathlib import Path

import cv2
import numpy as np


MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "ESPCN_x2.pb"
MODEL_NAME = "espcn"
MODEL_SCALE = 2
MAX_INPUT_EDGE = 1600

_sr_engine = None
_sr_available = False
_sr_failure_reason = None


def _load_super_resolution_engine():
    global _sr_engine, _sr_available, _sr_failure_reason

    if _sr_engine is not None or _sr_failure_reason is not None:
        return _sr_engine

    if not hasattr(cv2, "dnn_superres"):
        _sr_failure_reason = "OpenCV dnn_superres module is unavailable."
        return None

    if not MODEL_PATH.exists() or MODEL_PATH.stat().st_size == 0:
        _sr_failure_reason = "ESPCN model file is missing or empty."
        return None

    try:
        sr = cv2.dnn_superres.DnnSuperResImpl_create()
        sr.readModel(str(MODEL_PATH))
        sr.setModel(MODEL_NAME, MODEL_SCALE)
        _sr_engine = sr
        _sr_available = True
        return _sr_engine
    except Exception as exc:
        _sr_failure_reason = str(exc)
        return None


def super_resolution_available() -> bool:
    return _load_super_resolution_engine() is not None and _sr_available


def get_super_resolution_status() -> dict:
    _load_super_resolution_engine()
    return {
        "available": _sr_available,
        "model_path": str(MODEL_PATH),
        "reason": _sr_failure_reason,
    }


def upscale_image(image: np.ndarray) -> np.ndarray:
    engine = _load_super_resolution_engine()
    if engine is None or image is None:
        return image

    height, width = image.shape[:2]
    longest_edge = max(height, width)
    if longest_edge > MAX_INPUT_EDGE:
        scale = MAX_INPUT_EDGE / float(longest_edge)
        working = cv2.resize(
            image,
            None,
            fx=scale,
            fy=scale,
            interpolation=cv2.INTER_AREA,
        )
        upscaled = engine.upsample(working)
        return cv2.resize(
            upscaled,
            (width * MODEL_SCALE, height * MODEL_SCALE),
            interpolation=cv2.INTER_CUBIC,
        )

    return engine.upsample(image)
