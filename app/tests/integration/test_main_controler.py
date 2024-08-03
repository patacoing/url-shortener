from fastapi.testclient import TestClient
from fastapi import status
import pytest

from app.database.redis import RedisDatabase
from app.main import app
from app.service.rate_limit_service import RateLimitService
from app.service.url_service import UrlService
from app.settings import settings


@pytest.fixture
def database():
    db = RedisDatabase(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        password=settings.REDIS_PASSWORD
    )

    yield db

    db.redis.flushall()


@pytest.fixture
def url_service(monkeypatch, database):
    test_url_service = UrlService(database)

    monkeypatch.setattr(
        "app.service.url_service.get_url_service",
        lambda: test_url_service
    )

    return test_url_service


@pytest.fixture
def client(url_service):
    return TestClient(app, follow_redirects=False)


def test_shorten_url_should_return_401_when_client_is_under_limit(client, database):
    response = client.post("?url=http://test.com")

    assert response.status_code == status.HTTP_201_CREATED
    key = response.json()
    assert database.get_url(key) == "http://test.com/"


def test_shorten_url_should_return_403_when_client_is_above_limit(client, database):
    RateLimitService.limit = 0
    database.increase_call_count("testclient")
    response = client.post("?url=http://test.com")

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_url_should_redirect(client, database):
    database.save_url("test", "http://test.com/")
    response = client.get("test")

    assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
    assert response.headers["location"] == "http://test.com/"






