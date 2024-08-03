from unittest.mock import Mock

import pytest
from pydantic_core import Url
from fastapi import Request
from fastapi.responses import RedirectResponse

from app.exceptions.call_count_exceeded_exception import CallCountExceededException
from app.exceptions.key_not_found_exception import KeyNotFoundException
from app.service.url_service import UrlService, get_url_service

@pytest.fixture
def url_service():
    return UrlService(Mock())


def test_retrieve_url_should_raise_key_not_found_exception(url_service):
    url_service.database.get_url.return_value = None

    with pytest.raises(KeyNotFoundException):
        url_service.retrieve_url("test", Mock())


def test_retrieve_url_should_return_redirect_response(url_service):
    url_service.database.get_url.return_value = "http://test.com"

    response = url_service.retrieve_url("test", Mock())

    assert isinstance(response, RedirectResponse)


def test_shorten_url(monkeypatch, url_service):
    mock_key_generator_service = Mock()
    mock_key_generator_service.generate_key.return_value = "test"
    monkeypatch.setattr("app.service.url_service.KeyGeneratorService", mock_key_generator_service)

    shortened_url = url_service.shorten_url(Url("http://test.com"))

    assert shortened_url == "test"


def test_save_url(url_service):
    url = url_service.save_url("test", "http://test.com")

    url_service.database.save_url.assert_called_once()
    assert url == "http://test.com"


def test_shorten_and_save_url_should_return_key_when_client_is_under_limit(url_service, monkeypatch):
    url_service.shorten_url = Mock(return_value="test")
    url_service.save_url = Mock()
    mock_rate_limit_service = Mock()
    monkeypatch.setattr("app.service.url_service.RateLimitService", mock_rate_limit_service)
    mock_rate_limit_service.return_value.is_client_above_limit.return_value = False

    key = url_service.shorten_and_save_url(
        Url("http://test.com"),
        Request(scope=
            {
                "type": "http",
                "method": "POST",
                "path": "/",
                "client": ("test", 1234)
            }
        )
    )

    url_service.shorten_url.assert_called_once()
    url_service.save_url.assert_called_once()
    assert key == "test"


def test_shorten_and_save_url_should_raise_exception_when_client_is_above_limit(url_service, monkeypatch):
    mock_rate_limit_service = Mock()
    mock_rate_limit_service.return_value.is_client_above_limit.return_value = True
    monkeypatch.setattr("app.service.url_service.RateLimitService", mock_rate_limit_service)

    with pytest.raises(CallCountExceededException):

        url_service.shorten_and_save_url(
            Url("http://test.com"),
            Request(scope=
                {
                    "type": "http",
                    "method": "POST",
                    "path": "/",
                    "client": ("test", 1234)
                }
            )
        )
        mock_rate_limit_service.is_client_above_limit.assert_called_once()


def test_get_url_service():
    assert isinstance(get_url_service(), UrlService)