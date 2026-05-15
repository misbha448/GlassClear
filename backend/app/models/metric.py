from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from datetime import datetime
from app.core.database import Base


class Metric(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True)
    prediction_id = Column(Integer, ForeignKey("predictions.id"))

    psnr = Column(Float, nullable=True)
    ssim = Column(Float, nullable=True)
    lpips = Column(Float, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)