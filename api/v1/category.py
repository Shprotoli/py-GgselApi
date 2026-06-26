from abc import ABC

from api.client import SyncGClient, AsyncGClient

GClientType = SyncGClient | AsyncGClient


class Category(ABC):
    def __init__(self, client: GClientType):
        self.client = client
