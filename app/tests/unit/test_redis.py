from unittest.mock import Mock

import pytest

from app.database.redis import RedisDatabase
from app.settings import settings


@pytest.fixture
def redis_database(monkeypatch):
    monkeypatch.setattr("app.database.redis.Redis", Mock())

    return RedisDatabase()


def test_get_url(redis_database):
    redis_database.redis.get.return_value = b"http://test.com"

    result = redis_database.get_url("test")

    assert result == "http://test.com"
    assert redis_database.redis.get.called_once_with("test")


def test_get_url_should_return_none(redis_database):
    redis_database.redis.get.return_value = None

    result = redis_database.get_url("test")

    assert result is None

def test_save_url(redis_database):
    redis_database.redis.set.return_value = True

    result = redis_database.save_url("test", "http://test.com")

    assert result is True
    assert redis_database.redis.set.called_once_with(
        name="test",
        value="http://test.com",
        ex=settings.URL_VALIDITY_TIME
    )