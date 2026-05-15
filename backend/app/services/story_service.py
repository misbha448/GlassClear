from __future__ import annotations

import os

from app.models.prediction import Prediction

try:
    from PIL import Image
except ImportError:  # pragma: no cover
    Image = None


def _build_fallback_story(mode: str, ssim: float, edge_score: float, ai_reason: str, prediction: Prediction) -> str:
    scene_hint = "through a reflective glass surface in an architectural or outdoor setting"
    reflection_hint = "noticeable glare and layered reflections"
    improvement_hint = "removed the distraction while preserving natural textures and structural detail"

    if mode.lower() == "quality":
        improvement_hint = "reconstructed fine details while reducing harsh reflective artifacts"
    elif mode.lower() == "fidelity":
        improvement_hint = "softened glare while maintaining realistic tones and edge detail"

    if ssim >= 0.9:
        improvement_hint += " with strong visual consistency"
    if edge_score >= 0.85:
        improvement_hint += " and crisp edge retention"
    if prediction.processing_time and prediction.processing_time < 5:
        improvement_hint += " in a fast post-processing pass"
    if ai_reason:
        reflection_hint = ai_reason.lower().rstrip(".")

    return (
        f"This image appears to be captured {scene_hint}. "
        f"The AI detected {reflection_hint} and {improvement_hint}."
    )


def generate_story_for_prediction(
    model,
    prediction: Prediction,
    ai_mode: str,
    ssim: float,
    edge_score: float,
    ai_reason: str = ""
) -> str:
    fallback_story = _build_fallback_story(ai_mode, ssim, edge_score, ai_reason, prediction)

    if Image is None:
        return fallback_story

    # Normalize paths to handle OS-specific separators (\ vs /)
    original_path = os.path.normpath(prediction.original_image_path)
    processed_path = os.path.normpath(prediction.output_image_path)

    if not original_path or not processed_path:
        return fallback_story

    if not os.path.exists(original_path) or not os.path.exists(processed_path):
        print(f"STORY GEN ERROR: Files not found. Orig: {original_path}, Proc: {processed_path}")
        return fallback_story

    try:
        with Image.open(original_path).convert("RGB") as original_image, Image.open(processed_path).convert("RGB") as processed_image:
            width, height = original_image.size
            prompt = (
                "Analyze this original image and its cleaned result from a reflection removal system. "
                "Write one short polished description in no more than 2 sentences and keep it under 220 characters if possible. "
                "Mention the likely scene type, the kind of reflection or glare present, and what the AI improved. "
                f"Use this metadata when helpful: mode={ai_mode}, ssim={ssim:.3f}, edge_score={edge_score:.3f}, "
                f"processing_time={prediction.processing_time}, image_size={prediction.image_size}, dimensions={width}x{height}, "
                f"ai_reason={ai_reason or prediction.processing_mode}. "
                "Keep it concise for a premium UI card. Do not use bullet points, markdown, or quotation marks."
            )

            # Pass as a single list: [prompt, image1, image2]
            response = model.generate_content([prompt, original_image, processed_image])
            text = (getattr(response, "text", "") or "").strip()

            if not text:
                return fallback_story

            text = " ".join(text.split())
            if len(text) > 220:
                text = text[:220].rstrip(" ,.;") + "."
            return text
    except Exception as e:
        print(f"STORY GEN ERROR: {str(e)}")
        return fallback_story
