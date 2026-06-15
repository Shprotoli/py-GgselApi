from api.client import GClient
from api.v1.api_login import ApiLogin
from api.v1.account import Account
from api.v1.categories import Categories


class GgselApiV1:
    __objects_instance = ("_api_instance", "_account_instance", "_categories_instance")
    __slots__ = ["_client", *__objects_instance]

    def __init__(self, token: str = "", client: GClient | None = None):
        self._client = client or GClient()
        self._client.set_token(token)

    @property
    def api_login(self):
        if not hasattr(self, "_api_instance"):
            self._api_instance = ApiLogin(self._client)
        return self._api_instance

    @property
    def account(self):
        if not hasattr(self, "_account_instance"):
            self._account_instance = Account(self._client)
        return self._account_instance

    @property
    def categories(self):
        if not hasattr(self, "_categories_instance"):
            self._categories_instance = Categories(self._client)
        return self._categories_instance

    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, value: GClient):
        self._client = value

        for obj_name in filter(lambda obj: hasattr(self, obj), self.__objects_instance):
            obj_instance = getattr(self, obj_name)
            obj_instance.client = self._client

    def set_token(self, token: str) -> None:
        self._client.set_token(token)
