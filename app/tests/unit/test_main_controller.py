from unittest.mock import Mock
from fastapi import Response
from pydantic_core import Url

from app.controller.main_controller import get_url, shorten_url

def test_get_url(monkeypatch):
    mock_url_service = Mock()
    monkeypatch.setattr("app.controller.main_controller.UrlService", mock_url_service)

    get_url("test", Response(), mock_url_service)

    mock_url_service.retrieve_url.assert_called_once()


def test_shorten_url(monkeypatch):
    mock_url_service = Mock()
    monkeypatch.setattr("app.controller.main_controller.UrlService", mock_url_service)

    shorten_url(Url("http://test.com"), mock_url_service)

    mock_url_service.shorten_and_save_url.assert_called_once()