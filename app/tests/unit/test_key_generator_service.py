from pydantic_core import Url

from app.service.key_generator_service import KeyGeneratorService
from app.settings import settings

def test_generate_key():
    key = KeyGeneratorService.generate_key(Url("http://test.com"))

    assert len(key) == settings.URL_LENGTH