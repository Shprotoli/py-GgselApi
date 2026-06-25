from typing import Optional

from api.client import GClient, SyncGClient, AsyncGClient
from api.v1.api_login import ApiLogin, AsyncApiLogin
from api.v1.account import Account, AsyncAccount
from api.v1.categories import Categories, AsyncCategories
from api.v1.chats import Chats
from api.v1.products import Products
from api.v1.orders import Orders
from api.v1.reviews import Reviews

SYNC_API_MAP = {
    "_api_login_instance": ApiLogin,
    "_account_instance": Account,
    "_categories_instance": Categories,
    "_chats_instance": Chats,
    "_products_instance": Products,
    "_orders_instance": Orders,
    "_reviews_instance": Reviews,
}

ASYNC_API_MAP = {
    "_api_login_instance": AsyncApiLogin,
}


class GgselApiV1:
    __objects_instance = (
        "_api_login_instance",
        "_account_instance",
        "_categories_instance",
        "_chats_instance",
        "_products_instance",
        "_orders_instance",
        "_reviews_instance",
    )
    __slots__ = ["_client", "__async__", *__objects_instance]

    def __init__(self, token: str = "", client: Optional[GClient] = None):
        self._client = client or SyncGClient()
        self._client.set_token(token)

        self.__async__ = self.check_client_async()

    @property
    def api_login(self):
        if not hasattr(self, "_api_login_instance"):
            ApiLoginCls = AsyncApiLogin if self.__async__ else ApiLogin
            self._api_login_instance = ApiLoginCls(self._client)
        return self._api_login_instance

    @property
    def account(self):
        if not hasattr(self, "_account_instance"):
            AccountLoginCls = AsyncAccount if self.__async__ else Account
            self._account_instance = AccountLoginCls(self._client)
        return self._account_instance

    @property
    def categories(self):
        if not hasattr(self, "_categories_instance"):
            CategoriesLoginCls = AsyncCategories if self.__async__ else Categories
            self._categories_instance = CategoriesLoginCls(self._client)
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
    def reviews(self):
        if not hasattr(self, "_reviews_instance"):
            self._reviews_instance = Reviews(self._client)
        return self._reviews_instance

    @property
    def client(self):
        return self._client

    def __update_client_instance(self):
        """
        This method replaces the `client` object in all instances with the client object in `GgselApiV1`
        """
        for obj_name in filter(lambda obj: hasattr(self, obj), self.__objects_instance):
            obj_instance = getattr(self, obj_name)
            obj_instance.client = self._client

    @client.setter
    def client(self, new_client: GClient):
        token = getattr(self._client, "token", None)

        self._client = new_client
        if token:
            self._client.set_token(token)

        """
        We check if the client has updated from synchronous to asynchronous and vice versa,
        and if it has, we change the instance types to the corresponding ones
        """
        pred_async_flag = self.__async__
        self.__async__ = self.check_client_async()
        if pred_async_flag != self.__async__:
            self.__update_mode_instance()
        else:
            self.__update_client_instance()

    def set_token(self, token: str) -> None:
        self._client.set_token(token)

    def check_client_async(self) -> bool:
        """
        This method checks and tells you whether the current `client` object is asynchronous

        :return: True if the `client` object is asynchronous, and False if it is synchronous
        """
        return isinstance(self._client, AsyncGClient)

    def __update_mode_instance(self) -> None:
        """
        This method updates the object type to the current mode type
        (determined by the current `client` mode, which can be synchronous or asynchronous)
        """
        for obj_name in filter(lambda obj: hasattr(self, obj), self.__objects_instance):
            instance_type = ASYNC_API_MAP[obj_name] if self.__async__ else SYNC_API_MAP[obj_name]
            setattr(self, obj_name, instance_type(self._client))
