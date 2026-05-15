from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String

from app.core.database import Base


class CollageAsset(Base):
    __tablename__ = "collages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    title = Column(String, nullable=False)
    layout_type = Column(String, nullable=False)
    image_ids = Column(JSON, nullable=False)
    output_path = Column(String, nullable=True)
    status = Column(String, default="draft", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
