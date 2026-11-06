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

# OWASP's minimum for PBKDF2-HMAC-SHA256. 210,000 is its figure for SHA-512, which
# is what this used to apply to SHA-256; existing hashes upgrade on next sign-in.
PBKDF2_ITERATIONS = 600_000
_LEGACY_ITERATIONS = 210_000

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


def _digest(password: str, salt: str, iterations: int) -> str:
    raw = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), iterations)
    return base64.b64encode(raw).decode()


def hash_password(password: str, salt: str | None = None) -> tuple[str, str]:
    salt = salt or secrets.token_hex(16)
    return salt, _digest(password, salt, PBKDF2_ITERATIONS)


def verify_password(password: str, salt: str, expected_hash: str) -> bool:
    return verify_and_upgrade(password, salt, expected_hash)[0]


def verify_and_upgrade(password: str, salt: str, expected_hash: str) -> tuple[bool, str | None]:
    """Check a password; return (matched, replacement hash if it used the old cost)."""
    if hmac.compare_digest(_digest(password, salt, PBKDF2_ITERATIONS), expected_hash):
        return True, None
    if hmac.compare_digest(_digest(password, salt, _LEGACY_ITERATIONS), expected_hash):
        return True, _digest(password, salt, PBKDF2_ITERATIONS)
    return False, None


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
    except (ValueError, KeyError, TypeError, json.JSONDecodeError):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Your session has expired. Please sign in again.")
