from typing import Any

from parameters.globals import Lang
from parameters.api import EnumCrudMethod
from api.category import Category, RouteApiV1


class OrdersBaseV1(Category, RouteApiV1):
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
            "method": EnumCrudMethod.GET,
            "route": "seller-last-sales",
            "params": params,
            "headers": headers
        }

    def _order_info(self, invoice_id: int, locale: str | Lang = Lang.RU) -> dict[str, Any]:
        headers = {
            "locale": locale,
        }

        return {
            "method": EnumCrudMethod.GET,
            "route": f"purchase/info/{invoice_id}",
            "headers": headers,
        }

    def _check_unique_code(self, unique_code: str) -> dict[str, Any]:
        return {
            "method": EnumCrudMethod.GET,
            "route": f"purchases/unique-code/{unique_code}",
        }
