"""Small, dependency-free authentication primitives for PRISM.

The application uses PBKDF2 password hashes and signed, expiring bearer tokens.
For a production deployment, set PRISM_AUTH_SECRET to a long random value and
replace SQLite with a managed database.
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import secrets
import time

from fastapi import HTTPException, status

TOKEN_TTL_SECONDS = 60 * 60 * 8
_SECRET = os.getenv("PRISM_AUTH_SECRET", "change-this-prism-development-secret").encode()


def hash_password(password: str, salt: str | None = None) -> tuple[str, str]:
    salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 210_000)
    return salt, base64.b64encode(digest).decode()


def verify_password(password: str, salt: str, expected_hash: str) -> bool:
    _, actual_hash = hash_password(password, salt)
    return hmac.compare_digest(actual_hash, expected_hash)


def _encode(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).decode().rstrip("=")


def _decode(value: str) -> bytes:
    return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))


def create_token(user_id: int, role: str) -> str:
    payload = _encode(json.dumps({"sub": user_id, "role": role, "exp": int(time.time()) + TOKEN_TTL_SECONDS}).encode())
    signature = _encode(hmac.new(_SECRET, payload.encode(), hashlib.sha256).digest())
    return f"{payload}.{signature}"


def read_token(value: str | None) -> dict:
    if not value or not value.startswith("Bearer "):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Sign in is required")
    try:
        payload, signature = value.removeprefix("Bearer ").split(".", 1)
        expected = _encode(hmac.new(_SECRET, payload.encode(), hashlib.sha256).digest())
        data = json.loads(_decode(payload))
        if not hmac.compare_digest(signature, expected) or data["exp"] < time.time():
            raise ValueError("expired or invalid")
        return data
    except (ValueError, KeyError, json.JSONDecodeError):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Your session has expired. Please sign in again.")
