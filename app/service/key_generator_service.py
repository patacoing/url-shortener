from abc import ABC, abstractmethod
from pydantic_core import Url
from string import ascii_letters
from random import choice

from app.settings import settings


class KeyGeneratorServiceInterface(ABC):
    @staticmethod
    @abstractmethod
    def generate_key(url: Url) -> str:
        """
        Generate a key for a URL

        :param url: The URL to generate a key for
        :return: The generated key
        """
        pass


class KeyGeneratorService(KeyGeneratorServiceInterface):
    @staticmethod
    def generate_key(url: Url) -> str:
        return ''.join(choice(ascii_letters) for _ in range(settings.URL_LENGTH))