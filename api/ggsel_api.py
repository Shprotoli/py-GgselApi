from api.client import GClient, SyncGClient, AsyncGClient
from api.v1.api_login import ApiLogin, AsyncApiLogin
from api.v1.account import Account, AsyncAccount
from api.v1.categories import Categories, AsyncCategories
from api.v1.chats import Chats, AsyncChats
from api.v1.products import Products, AsyncProducts
from api.v1.orders import Orders, AsyncOrders
from api.v1.reviews import Reviews, AsyncReviews
from api.v1.category import Category

API_OBJECTS: dict[str, tuple[type[Category], type[Category]]] = {
    "_api_login_instance": (ApiLogin, AsyncApiLogin),
    "_account_instance": (Account, AsyncAccount),
    "_categories_instance": (Categories, AsyncCategories),
    "_chats_instance": (Chats, AsyncChats),
    "_products_instance": (Products, AsyncProducts),
    "_orders_instance": (Orders, AsyncOrders),
    "_reviews_instance": (Reviews, AsyncReviews),
}


class GgselApi:
    _objects_instance: tuple[str, ...]

    def __init__(self, api_key: str = "", token: str = "", client: GClient | None = None):
        self._client = client or SyncGClient(
            headers={"Authorization": api_key}
        )
        self._client.set_token(token)

        self.__async__ = self.check_client_async()

    @property
    def client(self) -> GClient:
        return self._client

    @client.setter
    def client(self, new_client: GClient) -> None:
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
            self._update_mode_instance()
        else:
            self._update_client_instance()

    def set_token(self, token: str) -> None:
        self._client.set_token(token)

    def check_client_async(self) -> bool:
        """
        This method checks and tells you whether the current `client` object is asynchronous

        :return: True if the `client` object is asynchronous, and False if it is synchronous
        """
        return isinstance(self._client, AsyncGClient)

    def _update_client_instance(self) -> None:
        """
        This method replaces the `client` object in all instances with the client object in `GgselApiV1`
        """
        for obj_name in filter(lambda obj: hasattr(self, obj), self._objects_instance):
            obj_instance = getattr(self, obj_name)
            obj_instance.client = self._client

    def _update_mode_instance(self) -> None:
        """
        This method updates the object type to the current mode type
        (determined by the current `client` mode, which can be synchronous or asynchronous)
        """
        for obj_name in filter(lambda obj: hasattr(self, obj), self._objects_instance):
            sync_cls, async_cls = API_OBJECTS[obj_name]
            instance_type = async_cls if self.__async__ else sync_cls
            setattr(self, obj_name, instance_type(self._client))

    def _get_api_instance(self, instance_name: str) -> Category:
        """
        This method receives an API category instance
        and lazily initializes the instance if it has not been created yet

        :param instance_name: The name of the instance from `API_OBJECTS`
        :return: An initialized API category object that is an heir to `Category`
        """
        if not hasattr(self, instance_name):
            sync_cls, async_cls = API_OBJECTS[instance_name]
            api_class = async_cls if self.__async__ else sync_cls

            setattr(self, instance_name, api_class(self._client))
        return getattr(self, instance_name)


class GgselApiV1(GgselApi):
    _objects_instance = (
        "_api_login_instance",
        "_account_instance",
        "_categories_instance",
        "_chats_instance",
        "_products_instance",
        "_orders_instance",
        "_reviews_instance",
    )
    __slots__ = ["_client", "__async__", *_objects_instance]

    def __init__(self, token: str = "", client: GClient | None = None):
        super().__init__(token=token, client=client)

    @property
    def api_login(self) -> ApiLogin | AsyncApiLogin:
        return self._get_api_instance("_api_login_instance")

    @property
    def account(self) -> Account | AsyncAccount:
        return self._get_api_instance("_account_instance")

    @property
    def categories(self) -> Categories | AsyncCategories:
        return self._get_api_instance("_categories_instance")

    @property
    def chats(self) -> Chats | AsyncChats:
        return self._get_api_instance("_chats_instance")

    @property
    def products(self) -> Products | AsyncProducts:
        return self._get_api_instance("_products_instance")

    @property
    def orders(self) -> Orders | AsyncOrders:
        return self._get_api_instance("_orders_instance")

    @property
    def reviews(self) -> Reviews | AsyncReviews:
        return self._get_api_instance("_reviews_instance")


class GgselApiV2(GgselApi):
    _objects_instance: tuple[str, ...] = ()
    __slots__ = ["_client", "__async__", "__obj_api_v1", *_objects_instance]

    def __init__(self, api_key: str = "", token: str = "", client: GClient | None = None):
        super().__init__(api_key, token, client)

        self.__obj_api_v1 = GgselApiV1(token, self._client)

    @property
    def api_v1(self) -> GgselApiV1:
        return self.__obj_api_v1

    @GgselApi.client.setter
    def client(self, new_client: GClient) -> None:
        GgselApi.client.fset(self, new_client)
        self.__obj_api_v1.client = new_client
