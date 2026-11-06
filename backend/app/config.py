"""Deployment-mode configuration.

PRISM ships with a public demo: unauthenticated persona endpoints, a one-click
database reset, and `X-Demo-Teacher` header impersonation. Those are acceptable
for a judged demo and unacceptable for a classroom holding real children's data,
so they live behind a single explicit switch instead of being always-on.

Set `PRISM_DEMO_MODE=0` for any deployment with real learners. Doing so also
makes `PRISM_AUTH_SECRET` mandatory, since the development fallback secret is
published in this repository and would otherwise let anyone forge a teacher
token.
"""
from __future__ import annotations

import os

_TRUTHY = {"1", "true", "yes", "on"}


def demo_mode() -> bool:
    """True when demo-only conveniences are enabled (default: on)."""
    return os.getenv("PRISM_DEMO_MODE", "1").strip().lower() in _TRUTHY
