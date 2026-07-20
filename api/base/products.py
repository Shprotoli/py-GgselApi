from json import dumps
from typing import Any

from api.category import Category, RouteApiV1
from parameters.globals import Lang, Currency
from parameters.products import OrderDir, OrderCol


class ProductsBaseV1(Category, RouteApiV1):
    def _products_list(
            self,
            ids: list[int | str],
            page: int = 1,
            count: int = 10,
            lang: str | Lang = Lang.RU,
            locale: str | Lang = Lang.RU,
    ) -> dict[str, Any]:
        if not isinstance(ids, (list, tuple)):
            ids = [ids]

        params = {
            "ids": ",".join(map(str, ids)),
            "page": page,
            "count": count,
        }
        headers = {
            "lang": lang,
            "locale": locale,
        }

        return {
            "route": "products/list",
            "params": params,
            "headers": headers,
        }

    def _product_info(self, product_id: str) -> dict[str, Any]:
        return {
            "route": f"products/{product_id}/data",
        }

    def _products_seller(
            self,
            id_seller: int,
            order_col: str | OrderCol = OrderCol.ORDER_COL,
            order_dir: str | OrderDir = OrderDir.ASC,
            rows: int = 100,
            page: int = 1,
            currency: str | Currency = Currency.RUB,
            lang: str | Lang = Lang.RU,
            show_hidden: int | bool = False,
            owner_id: int = 0,
    ) -> dict[str, Any]:
        payload = {
            "id_seller": id_seller,
            "order_col": order_col,
            "order_dir": order_dir,
            "rows": rows,
            "page": page,
            "currency": currency,
            "lang": lang,
            "show_hidden": show_hidden,
            "owner_id": owner_id,
        }

        return {
            "route": "seller-goods",
            "data": dumps(payload),
        }
