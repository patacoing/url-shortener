from pydantic_settings import BaseSettings, SettingsConfigDict

class UrlSettings(BaseSettings):
    URL_LENGTH: int = 5
    URL_VALIDITY_TIME: int = 60 * 60

class RedisSettings(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str

class Settings(
    UrlSettings,
    RedisSettings,
    BaseSettings
):
    class Config(SettingsConfigDict):
        env_file = ".env"

settings = Settings()