# A class file that handles requests from the `Products` category of the GGSell API
from json import dumps

from tools.handlers import handler_response_api, ApiResult
from parameters.products import Variant, OrderDir, OrderCol
from parameters.globals import Lang, Currency
from schemas.offer_list_object import OfferListObject
from schemas.offer_object import OfferObject
from schemas.seller_goods_list_object import SellerGoodsListObject
from api.v1.category import Category


class Products(Category):
    """
    IMPORTANT: THIS METHOD DOES NOT WORK AND RETURNS INCORRECT ANSWERS

    Source docs: https://seller.ggsel.com/docs/updates-prices-of-products-and-variants-in-bulk
    def product_edit_prices(
            self,
            product_id: int,
            price: int,
            variants: list[Variant] = (),
    ) -> dict:
        payload = {
            "product_id": product_id,
            "price": price,
            "variants": [
                variant.as_dict() for variant in variants
            ],
        }

        response = self.client.post("product/edit/prices", data=payload)
        data = response.json()

        return data
    """

    def products_list(
            self,
            ids: str | int | list[str, int],
            page: int = 1,
            count: int = 10,
            lang: str | Lang = Lang.RU,
            locale: str | Lang = Lang.RU,
    ) -> ApiResult:
        """
        Source docs: https://seller.ggsel.com/docs/return-all-products
        The method gets a list of products based on the specified parameters

        :param ids: Comma separated product IDs
        :param page: Page
        :param count: Count products
        :param lang: The language of the goods
        :param locale: Localization of goods
        :return: dataclass OfferListObject containing a json response from the API
        """
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

        response = self.client.get("products/list", params=params, headers=headers)
        data = response.json()

        return handler_response_api(OfferListObject, data=data)

    def product_info(self, product_id: str) -> ApiResult:
        """
        Source docs: https://seller.ggsel.com/docs/return-product-info
        This method receives information about the product, and you must be the creator of the product.

        :param product_id: Your product ID
        :return: dataclass OfferObject containing a json response from the API
        """
        response = self.client.get(f"products/{product_id}/data")
        data = response.json()

        return handler_response_api(OfferObject, data)

    def products_seller(
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
    ) -> ApiResult:
        """
        IMPORTANT: CURRENTLY, THIS ROUTE HAS A BUG AND RETURNS YOUR PRODUCTS INSTEAD OF THE USER WHOSE ID IS SPECIFIED IN `ID_SELLER`

        Source docs: https://seller.ggsel.com/docs/return-all-products-for-seller
        Method for getting all user products without detailed information
        (if the product has additional price filters, they will NOT be displayed)

        :param [NOW WORKING] id_seller: Seller's ID
        :param order_col: Which field to sort by
        :param order_dir: Sorting direction
                            Possible values:
                            1) asc — ascending
                            2) desc — descending
        :param rows: How many items can be returned per request (limit)
        :param page: Page number (pagination)
        :param currency: What currency should prices be shown in
        :param lang: API Response Language
        :param show_hidden: [NOT WORKING] Show hidden products or not
        :param owner_id: [OBSOLETE] Owner ID (may differ from the seller)
        :return:
        """
        payload = dumps({
            "id_seller": id_seller,
            "order_col": order_col,
            "order_dir": order_dir,
            "rows": rows,
            "page": page,
            "currency": currency,
            "lang": lang,
            "show_hidden": show_hidden,
            "owner_id": owner_id,
        })

        response = self.client.post(f"seller-goods", data=payload)
        data = response.json()

        return handler_response_api(SellerGoodsListObject, data=data)
