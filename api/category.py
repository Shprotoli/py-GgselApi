from abc import ABC

from api.client import SyncGClient, AsyncGClient

GClientType = SyncGClient | AsyncGClient


class Category(ABC):
    """
    This class serves as a parent for API category classes (for example: `api_login`)
    """
    ROUTE: str

    def __init__(self, client: GClientType):
        self.client = client
