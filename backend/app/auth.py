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
import warnings

from fastapi import HTTPException, status

TOKEN_TTL_SECONDS = 60 * 60 * 8

_DEV_SECRET = "change-this-prism-development-secret"


def _load_secret() -> bytes:
    """Resolve the token signing secret, refusing the published fallback in production.

    The development secret is committed to this repository, so a deployment that
    signs real teacher tokens with it can be impersonated by anyone who reads the
    source. Outside demo mode a real secret is therefore required to boot.
    """
    from .config import demo_mode

    configured = os.getenv("PRISM_AUTH_SECRET", "").strip()
    if configured:
        return configured.encode()
    if not demo_mode():
        raise RuntimeError(
            "PRISM_AUTH_SECRET must be set when PRISM_DEMO_MODE=0. Generate one with "
            "`python -c \"import secrets; print(secrets.token_urlsafe(48))\"`."
        )
    warnings.warn(
        "PRISM_AUTH_SECRET is unset; using the public development secret. "
        "This is safe for the local demo only.",
        RuntimeWarning,
        stacklevel=2,
    )
    return _DEV_SECRET.encode()


_SECRET = _load_secret()


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
