from datetime import datetime

from sqlalchemy import JSON, Boolean, Column, DateTime, ForeignKey, Integer, String

from app.core.database import Base


class EditVersion(Base):
    __tablename__ = "edit_versions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    image_id = Column(Integer, ForeignKey("predictions.id"), nullable=False, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    version_name = Column(String, nullable=False)
    version_type = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    settings = Column(JSON, nullable=True)
    ml_metadata = Column(JSON, nullable=True)
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
