# Requests of the `Products` category of the GGSel API
from ggsel_py.api.category import Category, AsyncCategory, RouteApiV1, RequestSpec, build_request, endpoint
from ggsel_py.parameters.api import EnumCrudMethod, Header
from ggsel_py.parameters.globals import Lang, Currency
from ggsel_py.parameters.products import OrderDir, OrderCol
from ggsel_py.schemas.v1.offer_list_object import OfferListObject
from ggsel_py.schemas.v1.offer_object import OfferObject
from ggsel_py.schemas.v1.seller_goods_list_object import SellerGoodsListObject


class ProductsEndpointsV1(Category, RouteApiV1):
    """
    `product_edit_prices` (https://seller.ggsel.com/docs/updates-prices-of-products-and-variants-in-bulk)
    is intentionally missing: the route does not work and returns incorrect answers
    """

    @endpoint(OfferListObject)
    def all_products(
            self,
            ids: list[int | str] | str | int,
            page: int = 1,
            count: int = 10,
            lang: str | Lang = Lang.RU,
            locale: str | Lang = Lang.RU,
    ) -> RequestSpec:
        """
        Source docs: https://seller.ggsel.com/docs/return-all-products
        The method gets a list of products by the specified ids in the `ids` argument

        :param ids: A product ID or a list of them
        """
        if not isinstance(ids, (list, tuple)):
            ids = [ids]

        params = {
            "ids": ",".join(map(str, ids)),
            "page": page,
            "count": count,
        }
        headers = {
            Header.LANG: str(lang),
            Header.LOCALE: str(locale),
        }

        return build_request(EnumCrudMethod.GET, "products/list", params=params, headers=headers)

    @endpoint(OfferObject)
    def product_info(self, product_id: str | int) -> RequestSpec:
        """
        Source docs: https://seller.ggsel.com/docs/return-product-info
        This method receives information about the product, and you must be the creator of the product.
        """
        return build_request(EnumCrudMethod.GET, f"products/{product_id}/data")

    @endpoint(SellerGoodsListObject)
    def all_products_for_seller(
            self,
            id_seller: int | None = None,
            order_col: str | OrderCol = OrderCol.ORDER_COL,
            order_dir: str | OrderDir = OrderDir.ASC,
            rows: int = 100,
            page: int = 1,
            currency: str | Currency = Currency.RUB,
            lang: str | Lang = Lang.RU,
            show_hidden: int | bool = False,
            owner_id: int = 0,
    ) -> RequestSpec:
        """
        IMPORTANT: CURRENTLY, THIS ROUTE HAS A BUG AND RETURNS YOUR PRODUCTS INSTEAD OF THE USER WHOSE ID IS SPECIFIED IN `ID_SELLER`

        Source docs: https://seller.ggsel.com/docs/return-all-products-for-seller
        Method for getting all user products without detailed information
        (if the product has additional price filters, they will NOT be displayed)

        :param id_seller: [NOT WORKING] Seller's ID
        :param order_col: Which field to sort by
        :param rows: How many items can be returned per request (limit)
        :param show_hidden: [NOT WORKING] Show hidden products or not
        :param owner_id: [OBSOLETE] Owner ID (may differ from the seller)
        """
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

        return build_request(EnumCrudMethod.POST, "seller-goods", payload=payload)


class Products(ProductsEndpointsV1):
    pass


class AsyncProducts(AsyncCategory, ProductsEndpointsV1):
    pass
