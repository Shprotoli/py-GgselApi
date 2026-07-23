from json import dumps
from typing import Any

from api.category import Category, RouteApiV1, RouteApiV2
from parameters.globals import Lang, Currency, Locale
from parameters.api import EnumCrudMethod
from parameters.products import OrderDir, OrderCol, StatusProduct, ProductList, ProductParametr, ProductListType


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
            "method": EnumCrudMethod.GET,
            "route": "products/list",
            "params": params,
            "headers": headers,
        }

    def _product_info(self, product_id: str) -> dict[str, Any]:
        return {
            "method": EnumCrudMethod.GET,
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
            "method": EnumCrudMethod.POST,
            "route": "seller-goods",
            "data": dumps(payload),
        }


class ProductsBaseV2(Category, RouteApiV2):
    def _list_products(
            self,
            offer_id: int,
            status: StatusProduct | str,
            sort_column: str,
            sort_direction: OrderDir | str,
            locale: Locale | str,
    ) -> dict[str, Any]:
        params = {
            "status": status,
            "sort_column": sort_column,
            "sort_direction": sort_direction,
        }
        headers = {
            "locale": locale,
        }

        return {
            "method": EnumCrudMethod.GET,
            "route": f"offers/{offer_id}/products",
            "params": params,
            "headers": headers,
        }

    def _create_products(
            self,
            offer_id: int,
            locale: Locale | str,
            body: ProductListType | ProductParametr,
    ):
        params = {
            "offer_id": offer_id,
        }
        headers = {
            "locale": locale,
        }

        if isinstance(body, ProductList):
            body = body.asdict()
        elif isinstance(body, ProductParametr):
            body = ProductList([body]).asdict()

        return {
            "method": EnumCrudMethod.POST,
            "route": f"offers/{offer_id}/products",
            "params": params,
            "headers": headers,
            "data": dumps(body),
        }

    def _archive_products(
            self,
            offer_id: int,
            locale: Locale | str,
            product_ids: list[int] | int,
            delete_all: bool,
    ):
        params = {
            "offer_id": offer_id,
        }
        headers = {
            "locale": locale,
        }
        payloads = {
            "product_ids": product_ids,
            "delete_all": str(delete_all).lower(),
        }

        return {
            "method": EnumCrudMethod.DELETE,
            "route": f"offers/{offer_id}/products",
            "params": params,
            "headers": headers,
            "data": dumps(payloads),
        }

    def _list_splitted_products(
            self,
            offer_id: int,
            variant_id: int,
            status: StatusProduct | str,
            sort_column: str,
            sort_direction: OrderDir | str,
            locale: Locale | str,
    ):
        params = {
            "status": status,
            "sort_column": sort_column,
            "sort_direction": sort_direction,
        }
        headers = {
            "locale": locale,
        }

        return {
            "method": EnumCrudMethod.GET,
            "route": f"offers/{offer_id}/variants/{variant_id}/splitted_products",
            "params": params,
            "headers": headers,
        }

    def _create_splitted_products(
            self,
            offer_id: int,
            variant_id: int,
            locale: Locale | str,
            body: ProductListType | ProductParametr,
    ):
        params = {
            "offer_id": offer_id,
            "variant_id": variant_id,
        }
        headers = {
            "locale": locale,
        }

        if isinstance(body, ProductList):
            body = body.asdict()
        elif isinstance(body, ProductParametr):
            body = ProductList([body]).asdict()

        return {
            "method": EnumCrudMethod.POST,
            "route": f"offers/{offer_id}/variants/{variant_id}/splitted_products",
            "params": params,
            "headers": headers,
            "data": dumps(body),
        }

    def _archive_splitted_products(
            self,
            offer_id: int,
            variant_id: int,
            locale: Locale | str,
            product_ids: list[int] | int | None,
            delete_all: str,
    ):
        params = {
            "offer_id": offer_id,
            "variant_id": variant_id,
        }
        headers = {
            "locale": locale,
        }
        payloads = {
            "product_ids": product_ids,
            "delete_all": str(delete_all).lower(),
        }
        print(payloads)

        return {
            "method": EnumCrudMethod.DELETE,
            "route": f"offers/{offer_id}/variants/{variant_id}/splitted_products",
            "params": params,
            "headers": headers,
            "data": dumps(payloads),
        }
