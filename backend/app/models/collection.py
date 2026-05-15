from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, UniqueConstraint

from app.core.database import Base


class Collection(Base):
    __tablename__ = "collections"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class CollectionItem(Base):
    __tablename__ = "collection_items"
    __table_args__ = (UniqueConstraint("collection_id", "prediction_id", name="uq_collection_prediction"),)

    id = Column(Integer, primary_key=True, index=True)
    collection_id = Column(Integer, ForeignKey("collections.id"), nullable=False, index=True)
    prediction_id = Column(Integer, ForeignKey("predictions.id"), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
