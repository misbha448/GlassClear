import os
import uuid
import shutil
from typing import Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Body, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import mimetypes
from sqlalchemy.orm import Session
import google.generativeai as genai
import cv2
import numpy as np
from PIL import Image, UnidentifiedImageError

from app.utils.image_processing import enhance_image
from app.utils.export_utils import save_image_for_export
from app.utils.file_handler import generate_output_path
from app.utils.filename_generator import normalize_extension, normalize_mode
from app.utils.super_resolution import get_super_resolution_status
from app.core.config import settings
from app.core.schema_bootstrap import ensure_dashboard_schema
from app.core.database import engine, SessionLocal, get_db
from app.models.user import User
from app.core.security import hash_password
from app.api.deps import get_current_user_optional
from app.services.prediction_service import create_prediction, get_prediction_by_id
from app.services.inference_service import run_reflection_removal  # ✅ FIXED IMPORT
from app.services.story_service import generate_story_for_prediction
from app.services.enhance_service import create_enhanced_image
from app.services.variation_service import create_variation_images
from app.schemas.enhance import EnhanceRequest, EnhanceResponse
from app.schemas.story import StoryRequest, StoryResponse
from app.schemas.variation import VariationRequest, VariationResponse, VariationItem
from app.db.base import Base

from app.api.routes.auth import google_router as google_auth_router
from app.api.routes.auth import router as auth_router
from app.api.routes.users import router as users_router
from app.api.routes.predictions import router as predictions_router
from app.api.routes.admin import router as admin_router
from app.api.routes.albums import router as albums_router
from app.api.routes.collage import router as collage_router
from app.api.routes.dashboard import router as dashboard_router
from app.api.routes.editor import router as editor_router
from app.api.routes.export import router as export_router
from app.api.routes.projects import router as projects_router
from app.api.routes.collections import router as collections_router
from app.api.routes.delivery_packs import router as delivery_packs_router
from app.api.routes.share import router as share_router, share_links_router
from app.api.routes.collage_editor import router as collage_editor_router
from app.api.routes.batch import router as batch_router

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gemini
genai.configure(api_key=settings.GEMINI_API_KEY, transport='rest')
model = genai.GenerativeModel('gemini-2.5-flash')
super_resolution_status = get_super_resolution_status()

# Static uploads
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


def cleanup_files(*paths: str):
    for path in paths:
        if path and os.path.exists(path):
            os.remove(path)


def validate_uploaded_image(path: str) -> None:
    try:
        with Image.open(path) as image:
            image.verify()
    except (UnidentifiedImageError, OSError, ValueError) as exc:
        raise HTTPException(status_code=400, detail="Please upload a valid image.") from exc


def is_reflection_candidate(path: str) -> bool:
    image = cv2.imread(path, cv2.IMREAD_COLOR)
    if image is None:
        return False

    resized = image
    height, width = image.shape[:2]
    longest_side = max(height, width)
    if longest_side > 1400:
        scale = 1400.0 / float(longest_side)
        resized = cv2.resize(
            image,
            (max(1, int(width * scale)), max(1, int(height * scale))),
            interpolation=cv2.INTER_AREA,
        )

    hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 80, 180)
    laplacian = cv2.Laplacian(gray, cv2.CV_32F)
    lines = cv2.HoughLinesP(
        edges,
        1,
        np.pi / 180.0,
        threshold=70,
        minLineLength=max(30, int(min(resized.shape[:2]) * 0.08)),
        maxLineGap=12,
    )

    value_channel = hsv[:, :, 2]
    saturation_channel = hsv[:, :, 1]
    blue, green, red = cv2.split(resized.astype(np.float32))
    rg = np.abs(red - green)
    yb = np.abs(0.5 * (red + green) - blue)

    bright_ratio = float(np.mean(value_channel >= 215))
    glare_ratio = float(np.mean((value_channel >= 225) & (saturation_channel <= 70)))
    low_saturation_ratio = float(np.mean(saturation_channel <= 75))
    edge_density = float(np.mean(edges > 0))
    contrast_score = float(np.std(gray) / 255.0)
    texture_energy = float(np.mean(np.abs(laplacian)) / 255.0)
    line_density = float(0.0 if lines is None else min(len(lines), 120) / 120.0)
    colorfulness = float(
        (np.sqrt(np.std(rg) ** 2 + np.std(yb) ** 2) + (0.3 * np.sqrt(np.mean(rg) ** 2 + np.mean(yb) ** 2)))
        / 255.0
    )

    axis_aligned_line_count = 0
    long_line_count = 0
    if lines is not None:
        min_long_length = max(resized.shape[1], resized.shape[0]) * 0.18
        for line in lines:
            x1, y1, x2, y2 = line[0]
            dx = float(x2 - x1)
            dy = float(y2 - y1)
            length = float(np.hypot(dx, dy))
            if length >= min_long_length:
                long_line_count += 1
            angle = abs(np.degrees(np.arctan2(dy, dx)))
            angle = min(angle, abs(180.0 - angle))
            if angle <= 12.0 or abs(angle - 90.0) <= 12.0:
                axis_aligned_line_count += 1

    axis_aligned_ratio = float(axis_aligned_line_count / max(1, len(lines) if lines is not None else 1))
    architecture_signal = float(min(long_line_count / 12.0, 1.0) * 0.6 + min(axis_aligned_ratio, 1.0) * 0.4)

    reflective_signal = (
        glare_ratio * 5.5
        + bright_ratio * 1.4
        + low_saturation_ratio * 0.45
        + min(line_density * 0.7, 0.35)
        + min(edge_density * 2.0, 0.25)
        + min(contrast_score * 0.5, 0.15)
        + min(texture_energy * 0.4, 0.1)
    )

    has_architecture_like_structure = (
        (long_line_count >= 6 and axis_aligned_ratio >= 0.55)
        or architecture_signal >= 0.45
    )
    has_reflective_regions = glare_ratio >= 0.012 or (bright_ratio >= 0.1 and low_saturation_ratio >= 0.42)
    not_overly_colorful = colorfulness <= 0.24

    return has_architecture_like_structure and has_reflective_regions and not_overly_colorful and reflective_signal >= 0.24


def has_meaningful_reflection_change(
    original_path: str,
    processed_path: str,
    *,
    ssim_value: float,
    ssim_threshold: float = 0.985,
    pixel_diff_threshold: float = 0.012,
) -> bool:
    original = cv2.imread(original_path, cv2.IMREAD_COLOR)
    processed = cv2.imread(processed_path, cv2.IMREAD_COLOR)

    if original is None or processed is None:
        return True

    if original.shape[:2] != processed.shape[:2]:
        processed = cv2.resize(processed, (original.shape[1], original.shape[0]), interpolation=cv2.INTER_AREA)

    pixel_diff = float(np.abs(original.astype(np.float32) - processed.astype(np.float32)).mean() / 255.0)
    return not (ssim_value >= ssim_threshold or pixel_diff <= pixel_diff_threshold)


@app.post("/process-image")
async def process_image(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    mode: str = Form("clean"),
    output_format: str = Form(None),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    mode_lower = normalize_mode(mode)

    os.makedirs("uploads", exist_ok=True)
    os.makedirs(os.path.join("uploads", "original"), exist_ok=True)
    os.makedirs(os.path.join("uploads", "output"), exist_ok=True)

    ext = os.path.splitext(file.filename)[1]
    unique_id = uuid.uuid4().hex
    guest_image_token = unique_id if current_user is None else None
    target_extension = normalize_extension(output_format, file.filename)

    temp_input = os.path.join("uploads", "original", f"in_{unique_id}{ext}")
    output_dir = "uploads"

    try:
        # ✅ SAVE INPUT IMAGE
        with open(temp_input, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        validate_uploaded_image(temp_input)
        if not is_reflection_candidate(temp_input):
            cleanup_files(temp_input)
            raise HTTPException(status_code=400, detail="Please upload a valid image.")

        # 🔥 REAL MODEL CALL (RDNet)
        results = run_reflection_removal(temp_input, output_dir, unique_id)
        processed_path = results["final"]
        processing_time = results["time"]

        if not has_meaningful_reflection_change(
            temp_input,
            processed_path,
            ssim_value=float(results["metrics"]["ssim"]),
        ):
            cleanup_files(temp_input, processed_path, results["confidence"], *results["stages"])
            return JSONResponse(
                status_code=200,
                content={
                    "processing_required": False,
                    "message": "No reflection detected. Processing not required.",
                },
            )

        final_path = generate_output_path(
            original_filename=file.filename,
            mode=mode_lower,
            target_format=target_extension,
        )

        if mode_lower == "enhanced":
            final_path = enhance_image(processed_path, final_path)
        else:
            base_image = cv2.imread(processed_path, cv2.IMREAD_COLOR)
            if base_image is None:
                raise HTTPException(status_code=500, detail="Processed image could not be prepared for export.")
            final_path = save_image_for_export(base_image, final_path)

        # ✅ MEDIA TYPE
        media_type, _ = mimetypes.guess_type(final_path)
        if not media_type:
            media_type = "image/jpeg"

        # 🧹 CLEANUP
        # Note: We stop deleting temp_input here because the AI Story Generator needs the original image 
        # for context-aware analysis. Consider a periodic cleanup task for production.

        # 📊 SAVE TO DB
        image_size_str = f"{(os.path.getsize(final_path) / (1024 * 1024)):.2f} MB"

        prediction = create_prediction(
            db=db,
            user_id=current_user.id if current_user else None,
            original_image_path=temp_input,
            output_image_path=final_path,
            status_value="completed",
            model_name="RDNet",
            mode=mode_lower,
            image_size=image_size_str,
            processing_time=processing_time,
            original_filename=file.filename,
            stored_filename=os.path.basename(temp_input),
            mime_type=file.content_type or media_type,
            file_size=os.path.getsize(temp_input),
            source="dashboard" if current_user else "guest",
            guest_image_token=guest_image_token,
            active_workspace=bool(current_user),
        )

        reason = (
            "Enhanced mode applied subtle clarity tuning for a polished smartphone-style finish."
            if mode_lower == "enhanced"
            else "Clean mode preserved the reflection removal result without additional clarity tuning."
        )

        # ✅ Construct JSON Response
        response_payload = {
            "prediction_id": prediction.id,
            "original_image_url": f"/uploads/{os.path.relpath(temp_input, 'uploads').replace(os.sep, '/')}",
            "processed_image_url": f"/uploads/{os.path.relpath(final_path, 'uploads').replace(os.sep, '/')}",
            "confidence_map_url": f"/uploads/{os.path.basename(results['confidence'])}",
            "selected_mode": mode_lower,
            "download_filename": os.path.basename(final_path),
            "output_format": target_extension,
            "media_type": media_type,
            "super_resolution_active": super_resolution_status["available"],
            "reason": reason,
            "ssim": results["metrics"]["ssim"],
            "edge_score": results["metrics"]["edge_score"],
            "intermediate_outputs": [f"/uploads/{os.path.basename(p)}" for p in results["stages"]],
            "processing_steps": [
                {"name": "Upload received", "status": "completed"},
                {"name": "Reflection detection", "status": "completed"},
                {"name": "AI processing", "status": "completed"},
                {"name": "Output generated", "status": "completed"}
            ],
            "guest_image_token": guest_image_token,
        }

        print(f"DEBUG: Sending Response to Frontend: {response_payload}")
        return response_payload

    except Exception as e:
        cleanup_files(temp_input)
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/chat")
async def chat_with_ai(payload: dict = Body(...)):
    user_message = payload.get("message")
    if not user_message:
        raise HTTPException(status_code=400, detail="Message is required")

    try:
        prompt = f"You are GlassClear AI. Help with reflection removal. User: {user_message}"
        response = model.generate_content(prompt)
        return {"response": response.text if response.text else "I processed that, but have no words!"}
    except Exception as e:
        print(f"CHAT ERROR: {str(e)}")
        return {"response": "Bhai, AI is acting up. Check your API Key or Model name!"}


@app.post("/ai/story", response_model=StoryResponse)
async def generate_ai_story(
    payload: StoryRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    prediction = get_prediction_by_id(
        db=db,
        prediction_id=payload.prediction_id,
        user_id=current_user.id if current_user else None
    )

    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction record not found")

    story = generate_story_for_prediction(
        model=model,
        prediction=prediction,
        ai_mode=payload.ai_mode,
        ssim=payload.ssim,
        edge_score=payload.edge_score,
        ai_reason=payload.ai_reason
    )

    return StoryResponse(story=story)


@app.post("/ai/enhance", response_model=EnhanceResponse)
async def enhance_ai_output(
    payload: EnhanceRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    prediction = get_prediction_by_id(
        db=db,
        prediction_id=payload.prediction_id,
        user_id=current_user.id if current_user else None
    )

    if not prediction.output_image_path:
        raise HTTPException(status_code=404, detail="Processed image not found")

    enhanced_path = create_enhanced_image(prediction.output_image_path)
    return EnhanceResponse(enhanced_image_url=f"/uploads/{os.path.basename(enhanced_path)}")


@app.post("/ai/variations", response_model=VariationResponse)
async def generate_ai_variations(
    payload: VariationRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    prediction = get_prediction_by_id(
        db=db,
        prediction_id=payload.prediction_id,
        user_id=current_user.id if current_user else None
    )

    if not prediction.output_image_path:
        raise HTTPException(status_code=404, detail="Processed image not found")

    generated_variations = create_variation_images(prediction.output_image_path)
    variation_items = [
        VariationItem(
            key=variation["key"],
            label=variation["label"],
            image_url=f"/uploads/{os.path.basename(variation['path'])}"
        )
        for variation in generated_variations
    ]

    return VariationResponse(variations=variation_items)


def create_initial_admin():
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.email == "admin@example.com").first()
        if not admin:
            admin_user = User(
                name="admin",
                email="admin@example.com",
                password_hash=hash_password("admin123"),
                role="admin"
            )
            db.add(admin_user)
            db.commit()
            print("Admin created")
    finally:
        db.close()


Base.metadata.create_all(bind=engine)
ensure_dashboard_schema(engine)
create_initial_admin()

app.include_router(auth_router)
app.include_router(google_auth_router)
app.include_router(users_router)
app.include_router(predictions_router)
app.include_router(admin_router)
app.include_router(collage_router)
app.include_router(dashboard_router)
app.include_router(editor_router)
app.include_router(export_router)
app.include_router(projects_router)
app.include_router(collections_router)
app.include_router(albums_router)
app.include_router(delivery_packs_router)
app.include_router(share_router)
app.include_router(share_links_router)
app.include_router(collage_editor_router)
app.include_router(batch_router)


@app.get("/")
def root():
    return {
        "message": "Backend is running successfully",
        "model": "RDNet Integrated",
        "super_resolution": super_resolution_status,
    }
