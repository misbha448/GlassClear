from pydantic import BaseModel

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str  # Add this field so SvelteKit knows if it's an admin or user


class GoogleAuthResponse(TokenResponse):
    user_name: str | None = None
