from abc import ABC, abstractmethod

from app.database.database_interface import DatabaseInterface
from app.settings import settings

class RateLimitServiceInterface(ABC):
    @abstractmethod
    def increase_client_call_count(self) -> int:
        """
        Increase the number of call of an ip address

        :param host: the host
        :return: the new number of call made by the client
        """
        pass

    @classmethod
    @abstractmethod
    def is_count_above_limit(cls, count: int) -> bool:
        """
        Test if a call count is above the limit
        :param count: the number of call
        :return: True if it's above, false otherwise
        """
        pass

    @abstractmethod
    def is_client_above_limit(self) -> bool:
        """
        Test if the number of calls of a client is
        above the limit
        :return: True if it's above, false otherwise
        """
        pass


class RateLimitService(RateLimitServiceInterface):
    limit: int = settings.RATE_LIMIT

    def __init__(self, host: str, database: DatabaseInterface):
        self.host = host
        self.database = database

    @classmethod
    def is_count_above_limit(cls, count: int) -> bool:
        return count > cls.limit

    def increase_client_call_count(self) -> int:
        count = self.database.get_call_count(self.host)
        self.database.increase_call_count(self.host)
        return count + 1

    def is_client_above_limit(self) -> bool:
        count = self.database.get_call_count(self.host)
        return RateLimitService.is_count_above_limit(count)


