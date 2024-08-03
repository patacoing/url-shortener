from fastapi import APIRouter, Depends, Response, status
from pydantic_core import Url

from app.service.url_service import UrlService, get_url_service

router = APIRouter()

@router.get(
    path="/{key}",
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    summary="Redirect to the shortened URL",
)
def get_url(key: str, response: Response, url_service: UrlService = Depends(get_url_service)):
    return url_service.retrieve_url(key, response)

@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    summary="Shorten a URL",
    response_model=str,
)
def shorten_url(url: Url, url_service: UrlService = Depends(get_url_service)):
    return url_service.shorten_and_save_url(url)