from __future__ import annotations

import re

from email_validator import EmailNotValidError, validate_email as validate_email_address
from fastapi import HTTPException, status

NAME_PATTERN = re.compile(r"^[A-Za-z ]+$")


def collapse_spaces(value: str) -> str:
    return " ".join((value or "").strip().split())


def normalize_email(value: str) -> str:
    return (value or "").strip().lower()


def _raise(message: str) -> None:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)


def validate_name(value: str) -> str:
    normalized = collapse_spaces(value)
    if not normalized:
        _raise("Name is required.")
    if len(normalized) < 3:
        _raise("Name must be at least 3 characters.")
    if len(normalized) > 50:
        _raise("Name must be at most 50 characters.")
    if not NAME_PATTERN.fullmatch(normalized):
        _raise("Name must contain only alphabets and spaces.")
    return normalized


def validate_email(value: str) -> str:
    normalized = normalize_email(value)
    if not normalized:
        _raise("Enter a valid email address.")
    try:
        result = validate_email_address(normalized, check_deliverability=False)
    except EmailNotValidError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Enter a valid email address.") from exc
    return result.normalized.lower()


def validate_password(value: str) -> str:
    password = value or ""
    if len(password) < 8:
        _raise("Password must be at least 8 characters.")
    if len(password) > 64:
        _raise("Password must be at most 64 characters.")

    has_upper = any(char.isupper() for char in password)
    has_lower = any(char.islower() for char in password)
    has_number = any(char.isdigit() for char in password)
    has_special = any(not char.isalnum() for char in password)

    if not (has_upper and has_lower and has_number and has_special):
        _raise("Password must include uppercase, lowercase, number, and special character.")
    return password


def validate_login_email(value: str) -> str:
    return validate_email(value)


def validate_login_password(value: str) -> str:
    if not value:
        _raise("Password is required.")
    return value
