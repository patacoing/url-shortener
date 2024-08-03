from abc import ABC, abstractmethod

class DatabaseInterface(ABC):
    @abstractmethod
    def get_url(self, key: str) -> str | None:
        pass

    @abstractmethod
    def save_url(self, key: str, url: str) -> bool:
        pass

    @abstractmethod
    def get_call_count(self, host: str) -> int:
        pass

    @abstractmethod
    def increase_call_count(self, host: str) -> bool:
        pass