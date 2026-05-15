from sqlalchemy import Boolean, Column, DateTime, Integer, String
from datetime import datetime
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False, default="")
    role = Column(String, default="user")
    auth_provider = Column(String, nullable=False, default="local")
    google_id = Column(String, nullable=True, unique=True)
    avatar_url = Column(String, nullable=True)
    is_email_verified = Column(Boolean, nullable=False, default=False)
    status = Column(String, nullable=False, default="active")

    created_at = Column(DateTime, default=datetime.utcnow)
