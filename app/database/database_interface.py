from abc import ABC, abstractmethod

class DatabaseInterface(ABC):
    @abstractmethod
    def get_url(self, key: str) -> str | None:
        """
        Get the URL from the database
        :param key: The key to retrieve the URL
        :return: The URL as a string or None
        """
        pass

    @abstractmethod
    def save_url(self, key: str, url: str) -> bool:
        """
        Save the URL in the database
        :param key: The key associated with the URL
        :param url: The URL to save
        :return: True if the URL was saved successfully, False otherwise
        """
        pass

    @abstractmethod
    def get_call_count(self, host: str) -> int:
        """
        Get the number of calls made by the client
        :param host: The client's host
        :return: The number of calls made by the client
        """
        pass

    @abstractmethod
    def increase_call_count(self, host: str) -> bool:
        """
        Increase the number of calls made by the client
        :param host: The client's host
        :return: True if the call count was increased successfully, False otherwise
        """
        pass