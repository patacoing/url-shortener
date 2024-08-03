from unittest.mock import Mock

import pytest
from pydantic_core import Url
from fastapi.responses import RedirectResponse

from app.database.database_interface import DatabaseInterface
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

def test_shorten_and_save_url(url_service):
    url_service.shorten_url = Mock(return_value="test")
    url_service.save_url = Mock()

    key = url_service.shorten_and_save_url(Url("http://test.com"))

    url_service.shorten_url.assert_called_once()
    url_service.save_url.assert_called_once()
    assert key == "test"


def test_get_url_service():
    assert isinstance(get_url_service(), UrlService)