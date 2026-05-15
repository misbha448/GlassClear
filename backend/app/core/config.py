from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str
    APP_ENV: str

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    DATABASE_URL: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    GEMINI_API_KEY: str
    FRONTEND_URL: str = "http://localhost:5173"

    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/api/auth/google/callback"

    SMTP_HOST: str = Field(default="", validation_alias=AliasChoices("SMTP_HOST", "MAIL_HOST"))
    SMTP_PORT: int = 587
    SMTP_USER: str = Field(default="", validation_alias=AliasChoices("SMTP_USER", "SMTP_USERNAME", "MAIL_USERNAME"))
    SMTP_APP_PASSWORD: str = Field(default="", validation_alias=AliasChoices("SMTP_APP_PASSWORD", "SMTP_PASSWORD", "MAIL_PASSWORD"))
    SMTP_FROM_EMAIL: str = Field(default="", validation_alias=AliasChoices("SMTP_FROM_EMAIL", "MAIL_FROM"))
    SMTP_FROM_NAME: str = "GlassClear"

    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)


settings = Settings()
