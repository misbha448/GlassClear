import os
import shutil
from uuid import uuid4
from fastapi import UploadFile

from app.utils.filename_generator import generate_filename, normalize_extension, normalize_mode

ORIGINAL_DIR = "uploads/original"
OUTPUT_DIR = "uploads/output"

os.makedirs(ORIGINAL_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


def save_uploaded_file(file: UploadFile) -> str:
    file_extension = normalize_extension(None, file.filename)
    unique_filename = f"{uuid4().hex}.{file_extension}"
    file_path = os.path.join(ORIGINAL_DIR, unique_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return file_path


def generate_output_path(
    original_filename: str,
    mode: str,
    target_format: str | None = None,
    scene: str | None = None,
) -> str:
    extension = normalize_extension(target_format, original_filename)
    output_filename = generate_filename(
        mode=normalize_mode(mode),
        original_filename=original_filename,
        target_format=extension,
        output_dir=OUTPUT_DIR,
        scene=scene,
    )
    return os.path.join(OUTPUT_DIR, output_filename)
