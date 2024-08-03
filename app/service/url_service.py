from abc import ABC, abstractmethod
from pydantic_core import Url
from fastapi import Response, Request
from fastapi.responses import RedirectResponse

from app.database.database_interface import DatabaseInterface
from app.database.redis import database
from app.exceptions.call_count_exceeded_exception import CallCountExceededException
from app.exceptions.key_not_found_exception import KeyNotFoundException
from app.service.key_generator_service import KeyGeneratorService
from app.service.rate_limit_service import RateLimitServiceInterface, RateLimitService


class UrlServiceInterface(ABC):
    def __init__(self, database: DatabaseInterface,):
        self.database = database

    @abstractmethod
    def retrieve_url(self, key: str, response: Response) -> RedirectResponse:
        """
        Retrieve a URL from the database

        :param key: The key to retrieve the URL
        :param response: The response object
        :return: The redirect response
        """
        pass

    @abstractmethod
    def shorten_url(self, url: Url) -> str:
        """
        Shorten a URL
        :param url: The URL to shorten
        :return: The shortened URL
        """
        pass

    @abstractmethod
    def save_url(self, key: str, url: str) -> str:
        """
        Save a URL in the database
        :param key: the generated key
        :param url: the url as a string
        :return: the url as a string
        """

    @abstractmethod
    def shorten_and_save_url(self, url: Url, request: Request) -> str:
        """
        Shorten and save a URL. It will before check whether the
        number of client calls is above the limit or not
        :param url: The URL to shorten and save
        :return: The shortened URL
        """


class UrlService(UrlServiceInterface):
    def retrieve_url(self, key: str, response: Response) -> RedirectResponse:
        content = self.database.get_url(key)
        if content is None:
            raise KeyNotFoundException(key)

        return RedirectResponse(content)

    def shorten_url(self, url: Url) -> str:
        return KeyGeneratorService.generate_key(url)

    def save_url(self, key: str, url: str) -> str:
        self.database.save_url(key, url)
        return url

    def shorten_and_save_url(self, url: Url, request: Request) -> str:
        host = request.client.host
        rate_limit_service: RateLimitServiceInterface = RateLimitService(host, self.database)

        if rate_limit_service.is_client_above_limit():
            raise CallCountExceededException()

        rate_limit_service.increase_client_call_count()
        key = self.shorten_url(url)
        self.save_url(key, str(url))
        return key

url_service = UrlService(database=database)

def get_url_service() -> UrlService:
    return url_service