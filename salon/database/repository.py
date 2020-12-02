from abc import ABC, abstractmethod


class RDFRepository(ABC):
    def __init__(self, endpoint: str, database: str, username: str = None, password: str = None):
        self.endpoint = endpoint
        self.database = database
        self.username = username
        self.password = password

    @abstractmethod
    async def query(self, query: str) -> dict:
        """
        Performs a query against the database.
        """
        pass

    @abstractmethod
    async def update(self, query: str) -> None:
        """
        Performs an update query against the database.
        """
        pass
