from fastapi.encoders import jsonable_encoder
from starlette.testclient import TestClient

from app.models.short import ShortCreate, ShortInfo
from app.tests.conftest import app_client, db_session, create_shorts


def test_create_short_link(app_client: TestClient, db_session):
    test_payload = ShortCreate(url="https://airbridge.io")
    response = app_client.post("/api/v1/shorts/short-links", json=jsonable_encoder(test_payload))
    response_json = response.json()

    assert response.status_code == 201
    assert ShortInfo(short_id=response_json["shortId"], url=response_json["url"], created_at=response_json["createdAt"])


def test_get_original_url(app_client: TestClient, db_session, create_shorts):
    response = app_client.get(f"/api/v1/shorts/short-links/3rc")
    response_json = response.json()

    assert response.status_code == 200
    assert ShortInfo(short_id=response_json["shortId"], url=response_json["url"], created_at=response_json["createdAt"])


def test_redirect_to_original(app_client: TestClient, db_session, create_shorts):
    # Case 1: Origin URL is not found in cache, found in database
    response = app_client.get("/api/v1/shorts/r/3rc", follow_redirects=False)

    assert response.status_code == 302
    assert response.headers["location"] == "https://airbridge.io"

    # Case 2: Origin URL is found in cache
    response = app_client.get("/api/v1/shorts/r/3rc", follow_redirects=False)

    assert response.status_code == 302
    assert response.headers["location"] == "https://airbridge.io"

    # Case 3: Origin URL is not found in cache & database
    response = app_client.get("/api/v1/shorts/r/abc", follow_redirects=False)

    assert response.status_code == 404
