from redis import Redis

from app.database.database_interface import DatabaseInterface
from app.settings import settings

class RedisDatabase(DatabaseInterface):
    def __init__(self,
        host: str = settings.REDIS_HOST,
        port: int = settings.REDIS_PORT,
        db: int = settings.REDIS_DB,
        password: str = settings.REDIS_PASSWORD
    ):
        self.redis: Redis = Redis(
            host=host,
            port=port,
            db=db,
            password=password
        )
    def get_url(self, key: str) -> str | None:
        result = self.redis.get(key)
        return result.decode("utf-8") if result else None

    def save_url(self, key: str, url: str) -> bool:
        return self.redis.set(
            name=key,
            value=url,
            ex=settings.URL_VALIDITY_TIME
        )

    def get_call_count(self, host: str) -> int:
        result = self.redis.get(host)
        return int(result) if result else 0

    def increase_call_count(self, host: str) -> bool:
        count = self.get_call_count(host)
        return self.redis.set(
            name=host,
            value=count+1,
            keepttl=True
        )

database = RedisDatabase()