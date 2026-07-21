from abc import ABC

from api.client import SyncGClient, AsyncGClient

GClientType = SyncGClient | AsyncGClient


class Route(ABC):
    ROUTE: str


class RouteApiV1:
    VERSION_ROUTE = "V1"
    ROUTE = "api_sellers/api"


class RouteApiV2:
    VERSION_ROUTE = "V2"
    ROUTE = "api_sellers/v2"


class Category(ABC):
    """
    This class serves as a parent for API category classes (for example: `api_login`)
    """

    def __init__(self, client: GClientType):
        self.client = client
