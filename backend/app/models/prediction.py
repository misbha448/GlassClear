from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Boolean
from datetime import datetime
from app.core.database import Base


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    original_image_path = Column(String, nullable=False)
    output_image_path = Column(String, nullable=True)

    status = Column(String, default="pending")
    model_name = Column(String, default="XReflection")
    processing_mode = Column(String, default="fidelity")
    image_size = Column(String, nullable=True)
    is_favorite = Column(Boolean, default=False)
    processing_time = Column(Float, nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    original_filename = Column(String, nullable=True)
    stored_filename = Column(String, nullable=True)
    mime_type = Column(String, nullable=True)
    file_size = Column(Integer, nullable=True)
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    source = Column(String, default="dashboard")
    guest_image_token = Column(String, unique=True, nullable=True)
    active_workspace = Column(Boolean, default=False)
    thumbnail_path = Column(String, nullable=True)
    category = Column(String, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    created_at = Column(DateTime, default=datetime.utcnow)
