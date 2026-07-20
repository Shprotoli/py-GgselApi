from typing import Any

from tools.handlers import handler_api, async_handler_api, EnumMethodHandle, ApiResult
from parameters.globals import Lang
from api.category import Category
from schemas.v1.last_sales_object import LastSalesObject
from schemas.v1.info_order_object import InfoOrderObject
from schemas.v1.unique_code_object import UniqueCodeObject


class OrdersBase(Category):
    def _last_sales(
            self,
            seller_id: int,
            group: bool = True,
            top: int = 10,
            locale: str | Lang = Lang.RU,
    ) -> dict[str, Any]:
        params = {
            "seller_id": seller_id,
            "group": group,
            "top": top,
        }
        headers = {
            "locale": locale,
        }

        return {
            "route": "seller-last-sales",
            "params": params,
            "headers": headers
        }

    def _order_info(self, invoice_id: int, locale: str | Lang = Lang.RU) -> dict[str, Any]:
        headers = {
            "locale": locale,
        }

        return {
            "route": f"purchase/info/{invoice_id}",
            "headers": headers,
        }

    def _check_unique_code(self, unique_code: str) -> dict[str, Any]:
        return {
            "route": f"purchases/unique-code/{unique_code}",
        }



class Orders(OrdersBase):
    def last_sales(
            self,
            seller_id: int,
            group: bool = True,
            top: int = 10,
            locale: str | Lang = Lang.RU,
    ) -> ApiResult:
        """
        Source docs: https://seller.ggsel.com/docs/return-last-sales
        This function gets a list of recent sales.
        The information is similar to the information on the page: `https://seller.ggsel.com/orders`

        :param seller_id: [NOW WORKING]
        :param group: [NOW WORKING]
        :param top: Number of entries
        :param locale: Localization of the returned information
        :return: dataclass LastSalesObject containing a json response from the API
        """
        return handler_api(
            EnumMethodHandle.GET,
            self.client,
            self._last_sales,
            LastSalesObject,
            seller_id=seller_id,
            group=group,
            top=top,
            locale=locale
        )

    def order_info(self, invoice_id: int, locale: str | Lang = Lang.RU) -> ApiResult:
        """
        Source docs: https://seller.ggsel.com/docs/get-order-info
        This method returns general information about the customer and what they have purchased.

        :param invoice_id: Unique order number
        :param locale: locale: Localization of the returned information
        :return: dataclass InfoOrderObject containing a json response from the API
        """
        return handler_api(
            EnumMethodHandle.GET,
            self.client,
            self._order_info,
            InfoOrderObject,
            invoice_id=invoice_id,
            locale=locale
        )

    def check_unique_code(self, unique_code: str) -> ApiResult:
        """
        Source docs: https://seller.ggsel.com/docs/check-unique-code
        Unlike `order_info`, this method returns more specific information about the product
        that the customer purchased using the unique order code.

        :param unique_code:
        :return:
        """
        return handler_api(
            EnumMethodHandle.GET,
            self.client,
            self._check_unique_code,
            UniqueCodeObject,
            unique_code=unique_code
        )


class AsyncOrders(OrdersBase):
    async def last_sales(
            self,
            seller_id: int,
            group: bool = True,
            top: int = 10,
            locale: str | Lang = Lang.RU,
    ) -> ApiResult:
        """
        See Orders.last_sales
        """
        return await async_handler_api(
            EnumMethodHandle.GET,
            self.client,
            self._last_sales,
            LastSalesObject,
            seller_id=seller_id,
            group=group,
            top=top,
            locale=locale
        )

    async def order_info(self, invoice_id: int, locale: str | Lang = Lang.RU) -> ApiResult:
        """
        See Orders.order_info
        """
        return await async_handler_api(
            EnumMethodHandle.GET,
            self.client,
            self._order_info,
            InfoOrderObject,
            invoice_id=invoice_id,
            locale=locale
        )

    async def check_unique_code(self, unique_code: str) -> ApiResult:
        """
        See Orders.check_unique_code
        """
        return await async_handler_api(
            EnumMethodHandle.GET,
            self.client,
            self._check_unique_code,
            UniqueCodeObject,
            unique_code=unique_code
        )
