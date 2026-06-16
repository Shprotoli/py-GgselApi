from api.client import GClient
from api.v1.api_login import ApiLogin
from api.v1.account import Account
from api.v1.categories import Categories
from api.v1.chats import Chats
from api.v1.products import Products
from api.v1.orders import Orders


class GgselApiV1:
    __objects_instance = (
        "_api_instance",
        "_account_instance",
        "_categories_instance",
        "_chats_instance",
        "_products_instance",
        "_orders_instance",
    )
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
    def chats(self):
        if not hasattr(self, "_chats_instance"):
            self._chats_instance = Chats(self._client)
        return self._chats_instance

    @property
    def products(self):
        if not hasattr(self, "_products_instance"):
            self._products_instance = Products(self._client)
        return self._products_instance

    @property
    def orders(self):
        if not hasattr(self, "_orders_instance"):
            self._orders_instance = Orders(self._client)
        return self._orders_instance

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
