from urllib.parse import urlencode

from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from app.schemas.user import UserResponse
from app.services.auth_service import (
    authenticate_local_user,
    build_auth_payload,
    build_google_login_url,
    exchange_google_code,
    fetch_google_user,
    get_or_create_google_user,
    register_local_user,
    validate_google_state,
)
from app.services.email_service import send_welcome_email

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])
google_router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse)
def register_user(payload: RegisterRequest, db: Session = Depends(get_db)):
    new_user = register_local_user(
        db,
        name=payload.name,
        email=str(payload.email),
        password=payload.password,
    )
    send_welcome_email(new_user.email, new_user.name)
    return new_user


@router.post("/login", response_model=TokenResponse)
def login_user(payload: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_local_user(db, str(payload.email), payload.password)
    return build_auth_payload(user)


@google_router.get("/google/login")
def google_login():
    return RedirectResponse(build_google_login_url(), status_code=302)


@google_router.get("/google/callback")
def google_callback(code: str | None = None, state: str | None = None, db: Session = Depends(get_db)):
    validate_google_state(state or "")
    token_data = exchange_google_code(code or "")
    google_profile = fetch_google_user(token_data.get("access_token", ""))
    user, is_new_user = get_or_create_google_user(db, google_profile)
    if is_new_user:
        send_welcome_email(user.email, user.name)

    auth_payload = build_auth_payload(user)
    redirect_query = urlencode(
        {
            "token": auth_payload["access_token"],
            "token_type": auth_payload["token_type"],
            "role": auth_payload["role"],
            "user_name": auth_payload["user_name"] or "",
        }
    )
    return RedirectResponse(f"{settings.FRONTEND_URL.rstrip('/')}/auth/callback?{redirect_query}", status_code=302)
