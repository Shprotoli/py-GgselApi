# A class file that handles requests from the `Products` category of the GGSell API
from tools.handlers import handler_api, async_handler_api, ApiResult
from parameters.products import OrderDir, OrderCol
from parameters.globals import Lang, Currency
from schemas.v1.offer_list_object import OfferListObject
from schemas.v1.offer_object import OfferObject
from schemas.v1.seller_goods_list_object import SellerGoodsListObject
from api.base.products import ProductsBaseV1


class Products(ProductsBaseV1):
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
            ids: list[int | str],
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
        return handler_api(
            self.client,
            self._products_list,
            OfferListObject,
            ids=ids,
            page=page,
            count=count,
            lang=lang,
            locale=locale
        )

    def product_info(self, product_id: str) -> ApiResult:
        """
        Source docs: https://seller.ggsel.com/docs/return-product-info
        This method receives information about the product, and you must be the creator of the product.

        :param product_id: Your product ID
        :return: dataclass OfferObject containing a json response from the API
        """
        return handler_api(
            self.client,
            self._product_info,
            OfferObject,
            product_id=product_id
        )

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
        return handler_api(
            self.client,
            self._products_seller,
            SellerGoodsListObject,
            id_seller=id_seller,
            order_col=order_col,
            order_dir=order_dir,
            rows=rows,
            page=page,
            currency=currency,
            lang=lang,
            show_hidden=show_hidden,
            owner_id=owner_id
        )


class AsyncProducts(ProductsBaseV1):
    async def products_list(
            self,
            ids: list[int | str],
            page: int = 1,
            count: int = 10,
            lang: str | Lang = Lang.RU,
            locale: str | Lang = Lang.RU,
    ) -> ApiResult:
        """
        See Products.products_list
        """
        return await async_handler_api(
            self.client,
            self._products_list,
            OfferListObject,
            ids=ids,
            page=page,
            count=count,
            lang=lang,
            locale=locale
        )

    async def product_info(self, product_id: str) -> ApiResult:
        """
        See Products.product_info
        """
        return await async_handler_api(
            self.client,
            self._product_info,
            OfferObject,
            product_id=product_id
        )

    async def products_seller(
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
        See Products.products_seller
        """
        return await async_handler_api(
            self.client,
            self._products_seller,
            SellerGoodsListObject,
            id_seller=id_seller,
            order_col=order_col,
            order_dir=order_dir,
            rows=rows,
            page=page,
            currency=currency,
            lang=lang,
            show_hidden=show_hidden,
            owner_id=owner_id
        )