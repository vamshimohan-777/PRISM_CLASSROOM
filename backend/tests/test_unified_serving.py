"""Verifies the single-service deployment: one FastAPI process serves both the
API and the built React SPA.

This is the contract render.yaml and the Dockerfile rely on. If the static
mount or the SPA fallback regresses, the deployed site serves a blank page
while every API test still passes, so it is worth asserting directly.

Skips when frontend/dist has not been built, so the backend suite still runs
on a machine without Node.
"""
import os
import pathlib

import pytest

os.environ.setdefault("DATABASE_URL", "sqlite:///./test_serving.db")

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
DIST = REPO_ROOT / "frontend" / "dist"

pytestmark = pytest.mark.skipif(
    not (DIST / "index.html").is_file(),
    reason="frontend/dist not built; run `npm run build` in frontend/",
)


@pytest.fixture(scope="module")
def client():
    from fastapi.testclient import TestClient

    from app.database import engine
    from app.main import app
    from app.seed import main as seed

    seed()
    with TestClient(app) as c:
        yield c
    engine.dispose()


def test_api_health_is_served(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_root_serves_the_spa(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert '<div id="root">' in response.text


@pytest.mark.parametrize("route", ["/curriculum", "/engines", "/flowchart", "/faq", "/app"])
def test_client_routes_fall_back_to_the_spa(client, route):
    """Deep links must return the app, not a 404, or a shared link breaks."""
    response = client.get(route)
    assert response.status_code == 200
    assert '<div id="root">' in response.text


def test_noscript_content_is_present_for_crawlers(client):
    response = client.get("/")
    assert "<noscript>" in response.text
    assert "PRISM Classroom" in response.text


def test_built_assets_are_served(client):
    """The hashed JS/CSS bundles must resolve, or the SPA loads blank."""
    assets = DIST / "assets"
    bundle = next((p for p in assets.iterdir() if p.suffix == ".js"), None)
    assert bundle is not None, "no JS bundle in frontend/dist/assets"
    response = client.get(f"/assets/{bundle.name}")
    assert response.status_code == 200
    assert response.content


def test_static_crawler_files_are_served(client):
    for path, needle in [
        ("/robots.txt", "Sitemap:"),
        ("/sitemap.xml", "<urlset"),
        ("/llms.txt", "PRISM Classroom"),
    ]:
        response = client.get(path)
        assert response.status_code == 200, path
        assert needle in response.text, path


def test_og_image_is_actually_present(client):
    """index.html advertises this image; a missing file breaks every preview card."""
    response = client.get("/prism-preview.png")
    assert response.status_code == 200
    assert response.content[:8] == b"\x89PNG\r\n\x1a\n"


@pytest.mark.parametrize("attack", [
    "../../../../etc/passwd",
    "assets/../../../../etc/passwd",
])
def test_traversal_attempts_never_escape_the_build_directory(client, attack):
    response = client.get("/" + attack)
    # Either the SPA shell or a refusal, but never file contents off the host.
    assert "root:x:0:0" not in response.text
