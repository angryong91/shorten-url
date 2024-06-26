from app.models.short import ShortCreate, ShortInfo, ShortCounts
from app.schemas import Shorts
from app.services.short import del_cache_url, set_cache_url
from app.tests.conftest import app_client, db_session, create_shorts
from fastapi.encoders import jsonable_encoder
from starlette.testclient import TestClient


def test_create_short_link(app_client: TestClient, db_session):
    test_payload = ShortCreate(url="https://airbridge.io")
    response = app_client.post("/api/v1/shorts/short-links", json=jsonable_encoder(test_payload))
    response_json = response.json()

    assert response.status_code == 201
    assert ShortInfo(short_id=response_json["shortId"], url=response_json["url"], created_at=response_json["createdAt"])

    Shorts.filter(id="3rc").delete()
    del_cache_url("3rc")


def test_get_original_url(app_client: TestClient, db_session, create_shorts):
    response = app_client.get(f"/api/v1/shorts/short-links/3rc")
    response_json = response.json()

    assert response.status_code == 200
    assert ShortInfo(short_id=response_json["shortId"], url=response_json["url"], created_at=response_json["createdAt"])


def test_redirect_to_original(app_client: TestClient, db_session):
    # Case 1: Origin URL is not found in cache & database
    response = app_client.get("/api/v1/shorts/r/3rc", follow_redirects=False)

    assert response.status_code == 404

    # Case 2: Origin URL is not found in cache, found in database
    Shorts.create(id="3rc", origin_url="https://airbridge.io")
    response = app_client.get("/api/v1/shorts/r/3rc", follow_redirects=False)

    assert response.status_code == 302
    assert response.headers["location"] == "https://airbridge.io"

    # Case 3: Origin URL is found in cache
    Shorts.filter(id="3rc").delete()
    set_cache_url("3rc", "https://airbridge.io")
    response = app_client.get("/api/v1/shorts/r/3rc", follow_redirects=False)

    assert response.status_code == 302
    assert response.headers["location"] == "https://airbridge.io"

    del_cache_url("3rc")


def test_count_shorts(app_client: TestClient, db_session, create_shorts):
    response = app_client.get("/api/v1/shorts/count/3rc")
    response_json = response.json()

    assert response.status_code == 200
    for d in response_json:
        assert ShortCounts(time=d["time"], count=d["count"])
