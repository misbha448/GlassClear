from __future__ import annotations

import json
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from fastapi import HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.services.auth_validation import (
    normalize_email,
    validate_email,
    validate_login_email,
    validate_login_password,
    validate_name,
    validate_password,
)

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"


def build_google_state() -> str:
    payload = {
        "scope": "google_oauth_state",
        "nonce": secrets.token_urlsafe(24),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=15),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def validate_google_state(state: str) -> None:
    try:
        payload = jwt.decode(state, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Google callback") from exc

    if payload.get("scope") != "google_oauth_state":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Google callback")


def build_google_login_url() -> str:
    if not settings.GOOGLE_CLIENT_ID or not settings.GOOGLE_REDIRECT_URI:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Google login is not configured")

    query = urlencode(
        {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "response_type": "code",
            "scope": "openid email profile",
            "access_type": "offline",
            "prompt": "select_account",
            "state": build_google_state(),
        }
    )
    return f"{GOOGLE_AUTH_URL}?{query}"


def _post_form(url: str, data: dict[str, Any]) -> dict[str, Any]:
    encoded = urlencode(data).encode("utf-8")
    request = Request(url, data=encoded, headers={"Content-Type": "application/x-www-form-urlencoded"}, method="POST")
    try:
        with urlopen(request, timeout=20) as response:
            return json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError) as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Google callback") from exc


def _get_json(url: str, headers: dict[str, str]) -> dict[str, Any]:
    request = Request(url, headers=headers, method="GET")
    try:
        with urlopen(request, timeout=20) as response:
            return json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError) as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Google callback") from exc


def exchange_google_code(code: str) -> dict[str, Any]:
    if not code:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Google callback")
    return _post_form(
        GOOGLE_TOKEN_URL,
        {
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        },
    )


def fetch_google_user(access_token: str) -> dict[str, Any]:
    if not access_token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Google callback")
    return _get_json(GOOGLE_USERINFO_URL, {"Authorization": f"Bearer {access_token}"})


def authenticate_local_user(db: Session, email: str, password: str) -> User:
    normalized_email = validate_login_email(email)
    validated_password = validate_login_password(password)
    user = db.query(User).filter(User.email == normalized_email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password.")
    if not user.password_hash or not verify_password(validated_password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password.")
    return user


def register_local_user(db: Session, *, name: str, email: str, password: str) -> User:
    normalized_name = validate_name(name)
    normalized_email = validate_email(email)
    validated_password = validate_password(password)

    existing_user = db.query(User).filter(User.email == normalized_email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered.")

    user = User(
        name=normalized_name,
        email=normalized_email,
        password_hash=hash_password(validated_password),
        role="user",
        auth_provider="local",
        is_email_verified=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_or_create_google_user(db: Session, google_profile: dict[str, Any]) -> tuple[User, bool]:
    email = normalize_email(google_profile.get("email") or "")
    google_id = google_profile.get("sub")
    if not email or not google_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Google callback")

    user = db.query(User).filter(User.email == email).first()
    is_new_user = False

    if user is None:
        user = User(
            name=google_profile.get("name") or email.split("@")[0],
            email=email,
            password_hash="",
            role="user",
            auth_provider="google",
            google_id=google_id,
            avatar_url=google_profile.get("picture"),
            is_email_verified=bool(google_profile.get("email_verified")),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        is_new_user = True
    else:
        user.google_id = user.google_id or google_id
        user.avatar_url = google_profile.get("picture") or user.avatar_url
        if user.auth_provider == "local":
            user.auth_provider = "google"
        user.is_email_verified = bool(google_profile.get("email_verified")) or user.is_email_verified
        db.commit()
        db.refresh(user)

    return user, is_new_user


def build_auth_payload(user: User) -> dict[str, Any]:
    access_token = create_access_token(data={"sub": str(user.id)})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": user.role,
        "user_name": user.name,
    }
