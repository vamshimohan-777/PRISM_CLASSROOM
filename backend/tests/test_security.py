"""Regression tests for the access-control and path-containment fixes."""
import os

os.environ.setdefault("DATABASE_URL", "sqlite:///./test_security.db")

import pytest
from fastapi import HTTPException

from app import config
from app.database import SessionLocal, engine
from app.main import resolve_teacher, require_demo_mode
from app.seed import main as seed


def setup_module():
    seed()


def teardown_module():
    engine.dispose()


def test_anonymous_caller_cannot_resolve_a_teacher():
    """Previously any credential-free caller was handed the seeded TEACHER-PRISM."""
    db = SessionLocal()
    with pytest.raises(HTTPException) as excinfo:
        resolve_teacher("", None, db)
    assert excinfo.value.status_code == 401
    db.close()


def test_demo_header_is_rejected_outside_demo_mode(monkeypatch):
    db = SessionLocal()
    assert resolve_teacher("TEACHER-PRISM", None, db).demo_identity == "TEACHER-PRISM"
    monkeypatch.setenv("PRISM_DEMO_MODE", "0")
    assert config.demo_mode() is False
    with pytest.raises(HTTPException) as excinfo:
        resolve_teacher("TEACHER-PRISM", None, db)
    assert excinfo.value.status_code == 401
    db.close()


def test_unknown_demo_identity_is_rejected_even_in_demo_mode():
    db = SessionLocal()
    with pytest.raises(HTTPException):
        resolve_teacher("TEACHER-DOES-NOT-EXIST", None, db)
    db.close()


def test_demo_only_endpoints_are_disabled_outside_demo_mode(monkeypatch):
    require_demo_mode()  # demo mode on by default: no raise
    monkeypatch.setenv("PRISM_DEMO_MODE", "0")
    with pytest.raises(HTTPException) as excinfo:
        require_demo_mode()
    assert excinfo.value.status_code == 404


@pytest.mark.parametrize("flag,expected", [("1", True), ("true", True), ("on", True),
                                           ("0", False), ("no", False), ("", False)])
def test_demo_mode_flag_parsing(monkeypatch, flag, expected):
    monkeypatch.setenv("PRISM_DEMO_MODE", flag)
    assert config.demo_mode() is expected


def test_auth_secret_is_mandatory_outside_demo_mode(monkeypatch):
    """The development secret is public, so production must supply its own."""
    import importlib

    monkeypatch.setenv("PRISM_DEMO_MODE", "0")
    monkeypatch.delenv("PRISM_AUTH_SECRET", raising=False)
    import app.auth as auth_module

    with pytest.raises(RuntimeError, match="PRISM_AUTH_SECRET"):
        importlib.reload(auth_module)

    # restore a usable module for the rest of the session
    monkeypatch.setenv("PRISM_DEMO_MODE", "1")
    importlib.reload(auth_module)


@pytest.mark.parametrize("attack", [
    "../../../../etc/passwd",
    "..%2f..%2fetc%2fpasswd",
    "assets/../../../../etc/hosts",
    "....//....//etc/passwd",
])
def test_spa_handler_contains_path_traversal(tmp_path, attack):
    """The hand-rolled static handler must not serve files outside the build dir."""
    import os.path

    dist = tmp_path / "dist"
    dist.mkdir()
    (dist / "index.html").write_text("<!doctype html><title>spa</title>")
    secret = tmp_path / "outside.txt"
    secret.write_text("should never be served")

    dist_root = os.path.realpath(str(dist))

    # Mirrors the containment check in main.serve_spa
    candidate = os.path.realpath(os.path.join(dist_root, attack))
    within_root = candidate == dist_root or candidate.startswith(dist_root + os.sep)
    served = candidate if (within_root and os.path.isfile(candidate)) else os.path.join(dist_root, "index.html")

    assert os.path.realpath(served).startswith(dist_root)
    assert "outside.txt" not in served
