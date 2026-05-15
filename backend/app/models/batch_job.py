from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String, Text

from app.core.database import Base


class BatchJob(Base):
    __tablename__ = "batch_jobs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    name = Column(String, nullable=False)
    status = Column(String, default="queued", nullable=False)
    total_count = Column(Integer, default=0)
    completed_count = Column(Integer, default=0)
    failed_count = Column(Integer, default=0)
    zip_path = Column(String, nullable=True)
    settings = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class BatchJobItem(Base):
    __tablename__ = "batch_job_items"

    id = Column(Integer, primary_key=True, index=True)
    batch_job_id = Column(Integer, ForeignKey("batch_jobs.id"), nullable=False, index=True)
    image_id = Column(Integer, ForeignKey("predictions.id"), nullable=False, index=True)
    status = Column(String, default="queued", nullable=False)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
