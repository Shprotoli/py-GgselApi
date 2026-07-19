from api.client import GClient, SyncGClient, AsyncGClient
# API V1 Category
from api.v1.api_login import (
    ApiLogin as ApiLoginV1,
    AsyncApiLogin as AsyncApiLoginV1,
)
from api.v1.account import (
    Account as AccountV1,
    AsyncAccount as AsyncAccountV1,
)
from api.v1.categories import (
    Categories as CategoriesV1,
    AsyncCategories as AsyncCategoriesV1,
)
from api.v1.chats import (
    Chats as ChatsV1,
    AsyncChats as AsyncChatsV1
)
from api.v1.products import (
    Products as ProductsV1,
    AsyncProducts as AsyncProductsV1,
)
from api.v1.orders import (
    Orders as OrdersV1,
    AsyncOrders as AsyncOrdersV1,
)
from api.v1.reviews import (
    Reviews as ReviewsV1,
    AsyncReviews as AsyncReviewsV1,
)
from api.category import Category
# API V2 Category
from api.v2.categories import (
    Categories as CategoriesV2,
    AsyncCategories as AsyncCategoriesV2,
)

API_V1_OBJECTS = {
    "_v1_api_login_instance": (ApiLoginV1, AsyncApiLoginV1),
    "_v1_account_instance": (AccountV1, AsyncAccountV1),
    "_v1_categories_instance": (CategoriesV1, AsyncCategoriesV1),
    "_v1_chats_instance": (ChatsV1, AsyncChatsV1),
    "_v1_products_instance": (ProductsV1, AsyncProductsV1),
    "_v1_orders_instance": (OrdersV1, AsyncOrdersV1),
    "_v1_reviews_instance": (ReviewsV1, AsyncReviewsV1),
}

API_V2_OBJECTS = {
    "_v2_categories_instance": (CategoriesV2, AsyncCategoriesV2),
}

API_OBJECTS: dict[str, tuple[type[Category], type[Category]]] = {
    **API_V1_OBJECTS,
    **API_V2_OBJECTS,
}


class CategoriesApiV1:
    @property
    def api_login(self) -> ApiLoginV1 | AsyncApiLoginV1:
        return self._get_api_instance("_v1_api_login_instance")

    @property
    def account(self) -> AccountV1 | AsyncAccountV1:
        return self._get_api_instance("_v1_account_instance")

    @property
    def categories(self) -> CategoriesV1 | AsyncCategoriesV1:
        return self._get_api_instance("_v1_categories_instance")

    @property
    def chats(self) -> ChatsV1 | AsyncChatsV1:
        return self._get_api_instance("_v1_chats_instance")

    @property
    def products(self) -> ProductsV1 | AsyncProductsV1:
        return self._get_api_instance("_v1_products_instance")

    @property
    def orders(self) -> OrdersV1 | AsyncOrdersV1:
        return self._get_api_instance("_v1_orders_instance")

    @property
    def reviews(self) -> ReviewsV1 | AsyncReviewsV1:
        return self._get_api_instance("_v1_reviews_instance")


class CategoriesApiV2(CategoriesApiV1):
    @property
    def categories(self) -> CategoriesV2 | AsyncCategoriesV2:
        return self._get_api_instance("_v2_categories_instance")


class GgselApi:
    _objects_instance: tuple[str, ...]

    def __init__(self, api_key: str = "", token: str = "", client: GClient | None = None):
        self._client = client or SyncGClient(
            headers={
                "Authorization": api_key
            },
        )
        self._client.set_token(token)

        self.__async__ = self.is_async()

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
        self.__async__ = self.is_async()
        if pred_async_flag != self.__async__:
            self._update_mode_instance()
        else:
            self._update_client_instance()

    def set_token(self, token: str) -> None:
        self._client.set_token(token)

    def is_async(self) -> bool:
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

            if hasattr(obj_instance, "ROUTE"):
                obj_instance.client._base_route = obj_instance.ROUTE

    def _update_mode_instance(self) -> None:
        """
        This method updates the object type to the current mode type
        (determined by the current `client` mode, which can be synchronous or asynchronous)
        """
        for obj_name in filter(lambda obj: hasattr(self, obj), self._objects_instance):
            sync_cls, async_cls = API_OBJECTS[obj_name]
            instance_type = async_cls if self.__async__ else sync_cls

            client = self._client
            if hasattr(instance_type, "ROUTE"):
                client._base_route = instance_type.ROUTE
            setattr(self, obj_name, instance_type(client))

    def _get_api_instance(self, instance_name: str) -> Category:
        """
        This method receives an API category instance
        and lazily initializes the instance if it has not been created yet

        :param instance_name: The name of the instance from `API_OBJECTS`
        :return: An initialized API category object that is an heir to `Category`
        """
        if not hasattr(self, instance_name):
            sync_cls, async_cls = API_OBJECTS[instance_name]
            instance_type = async_cls if self.__async__ else sync_cls

            client = self._client
            if hasattr(instance_type, "ROUTE"):
                client._base_route = instance_type.ROUTE
            setattr(self, instance_name, instance_type(client))
        return getattr(self, instance_name)


class GgselApiV1(GgselApi, CategoriesApiV1):
    _objects_instance: tuple[str, ...] = tuple(API_V1_OBJECTS.keys())
    __slots__ = ["_client", "__async__", *_objects_instance]

    def __init__(self, token: str = "", client: GClient | None = None):
        super().__init__(token=token, client=client)


class GgselApiV2(GgselApi, CategoriesApiV2):
    _objects_instance: tuple[str, ...] = tuple(API_V2_OBJECTS.keys())
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
