from pydantic_settings import BaseSettings, SettingsConfigDict

class UrlSettings(BaseSettings):
    URL_LENGTH: int = 5
    URL_VALIDITY_TIME: int = 60 * 60

class RateLimitSettings(BaseSettings):
    RATE_LIMIT: int = 10
    RATE_LIMIT_TIME: int = 60

class RedisSettings(BaseSettings):
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str

class AppSettings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000

class Settings(
    UrlSettings,
    RedisSettings,
    AppSettings,
    RateLimitSettings
):
    class Config(SettingsConfigDict):
        env_file = ".env"

settings = Settings()