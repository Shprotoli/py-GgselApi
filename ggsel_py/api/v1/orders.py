# Requests of the `Orders` category of the GGSel API
from ggsel_py.api.category import (
    Category, AsyncCategory, RouteApiV1, RequestSpec, build_request, endpoint, locale_header,
)
from ggsel_py.parameters.api import EnumCrudMethod
from ggsel_py.parameters.globals import Lang
from ggsel_py.schemas.v1.info_order_object import InfoOrderObject
from ggsel_py.schemas.v1.last_sales_object import LastSalesObject
from ggsel_py.schemas.v1.unique_code_object import UniqueCodeObject


class OrdersEndpointsV1(Category, RouteApiV1):
    @endpoint(LastSalesObject)
    def last_sales(
            self,
            seller_id: int | None = None,
            group: bool = True,
            top: int = 10,
            locale: str | Lang = Lang.RU,
    ) -> RequestSpec:
        """
        Source docs: https://seller.ggsel.com/docs/return-last-sales
        This function gets a list of recent sales.
        The information is similar to the information on the page: `https://seller.ggsel.com/orders`

        :param seller_id: [NOT WORKING]
        :param group: [NOT WORKING]
        :param top: Number of entries
        """
        params = {
            "seller_id": seller_id,
            "group": group,
            "top": top,
        }

        return build_request(EnumCrudMethod.GET, "seller-last-sales", params=params, headers=locale_header(locale))

    @endpoint(InfoOrderObject)
    def order_info(self, invoice_id: int, locale: str | Lang = Lang.RU) -> RequestSpec:
        """
        Source docs: https://seller.ggsel.com/docs/get-order-info
        This method returns general information about the customer and what they have purchased.
        """
        return build_request(EnumCrudMethod.GET, f"purchase/info/{invoice_id}", headers=locale_header(locale))

    @endpoint(UniqueCodeObject)
    def check_unique_code(self, unique_code: str) -> RequestSpec:
        """
        Source docs: https://seller.ggsel.com/docs/check-unique-code
        Unlike `order_info`, this method returns more specific information about the product
        that the customer purchased using the unique order code.
        """
        return build_request(EnumCrudMethod.GET, f"purchases/unique-code/{unique_code}")


class Orders(OrdersEndpointsV1):
    pass


class AsyncOrders(AsyncCategory, OrdersEndpointsV1):
    pass
