from parameters.globals import Locale
from tools.handlers import async_handler_api, handler_api, ApiResult
from api.base.products import ProductsBaseV2
from parameters.products import StatusProduct, OrderDir, ProductList, ProductParametr, ProductListType
from schemas.v2.list_of import ListOfProducts
from schemas.general_objects import SuccessObject


class Products(ProductsBaseV2):
    def list_products(
            self,
            offer_id: int,
            status: StatusProduct | str = StatusProduct.IN_STOCK,
            sort_column: str = "created_at",
            sort_direction: OrderDir | str = OrderDir.DESC,
            locale: Locale | str = "ru",
    ) -> ApiResult:
        """
        Source docs: https://seller.ggsel.com/docs/v2/list-products
        This method returns a list of items added to the product.

        :param offer_id: Product ID
        :param status: Product display type: `is_stock` or `sold`
        :param sort_column: Type column for sorted
        :param sort_direction: Direction sort
        :param locale: Localization response
        """
        return handler_api(
            self.client,
            self._list_products,
            ListOfProducts,
            offer_id=offer_id,
            status=status,
            sort_column=sort_column,
            sort_direction=sort_direction,
            locale=locale
        )

    def create_products(
            self,
            offer_id: int,
            body: ProductListType | ProductParametr,
            locale: Locale | str = "ru",
    ):
        """
        Source docs: https://seller.ggsel.com/docs/v2/create-products
        Using this method, you can add content to a product

        :param offer_id: Product ID
        :param body: The content of the product you want to add
        :param locale: Localization response
        """
        return handler_api(
            self.client,
            self._create_products,
            None,
            offer_id=offer_id,
            body=body,
            locale=locale
        )

    def archive_products(
            self,
            offer_id: int,
            product_ids: list[int] | int | None = None,
            locale: Locale | str = "ru",
            delete_all: bool = False,
    ):
        """
        Source docs: https://seller.ggsel.com/docs/v2/archive-products

        :param offer_id: Product ID
        :param product_ids: The ID of the product (or a list of product IDs) that you want to delete.
                            You can find the current product IDs using the `list_products` method
        :param locale: Localization response
        :param delete_all: Should I delete all the products - True or False.
                           If you want to delete all products, you should not pass anything (or pass `None`) in the `product_ids` field
        """
        return handler_api(
            self.client,
            self._archive_products,
            SuccessObject,
            offer_id=offer_id,
            product_ids=product_ids,
            delete_all=delete_all,
            locale=locale
        )

    def list_splitted_products(
            self,
            offer_id: int,
            variant_id: int,
            status: StatusProduct | str = StatusProduct.IN_STOCK,
            sort_column: str = "created_at",
            sort_direction: OrderDir | str = OrderDir.DESC,
            locale: Locale | str = "ru",
    ):
        """
        Source docs: https://seller.ggsel.com/docs/v2/archive-products
        This method returns the product content for splitted products by product ID and variant ID

        :param offer_id: Product ID
        :param variant_id: ID of the variant parameter for viewing the product content
        :param status: Product display status
        :param sort_column: Type column for sorted
        :param sort_direction: Direction sort
        :param locale: Localization response
        """
        return handler_api(
            self.client,
            self._list_splitted_products,
            ListOfProducts,
            offer_id=offer_id,
            variant_id=variant_id,
            status=status,
            sort_column=sort_column,
            sort_direction=sort_direction,
            locale=locale
        )

    def create_splitted_products(
            self,
            offer_id: int,
            variant_id: int,
            body: ProductListType | ProductParametr,
            locale: Locale | str = "ru",
    ):
        """
        Source docs: https://seller.ggsel.com/docs/v2/create-splitted-products
        This method adds the product content to a specific variant using the product ID and variant ID.

        :param offer_id: Product ID
        :param variant_id: ID of the variant parameter for viewing the product content
        :param body: The content of the product you want to add
        :param locale: Localization response
        """
        return handler_api(
            self.client,
            self._create_splitted_products,
            None,
            offer_id=offer_id,
            variant_id=variant_id,
            body=body,
            locale=locale
        )

    def archive_splitted_products(
            self,
            offer_id: int,
            variant_id: int,
            product_ids: list[int] | int | None = None,
            locale: Locale | str = "ru",
            delete_all: bool = False,
    ):
        """
        Source docs: https://seller.ggsel.com/docs/v2/archive-splitted-products
        This method removes a product (or products) by lot ID (`offer_id`), variant ID (`variant_id`), and product ID (`products_ids`)

        :param offer_id: Product ID
        :param variant_id: ID of the variant parameter for delete the product content
        :param product_ids: The ID of the product (or a list of product IDs) that you want to delete.
                            You can find the current product IDs using the `list_products` method
        :param locale: Localization response
        :param delete_all: Should I delete all the products - True or False.
                           If you want to delete all products, you should not pass anything (or pass `None`) in the `product_ids` field
        """
        return handler_api(
            self.client,
            self._archive_splitted_products,
            SuccessObject,
            offer_id=offer_id,
            variant_id=variant_id,
            product_ids=product_ids,
            delete_all=delete_all,
            locale=locale
        )


class AsyncProducts(ProductsBaseV2):
    async def list_products(
            self,
            offer_id: int,
            status: StatusProduct | str = StatusProduct.IN_STOCK,
            sort_column: str = "created_at",
            sort_direction: OrderDir | str = OrderDir.DESC,
            locale: Locale | str = "ru",
    ) -> ApiResult:
        """
        See Products.list_products
        """
        return await async_handler_api(
            self.client,
            self._list_products,
            ListOfProducts,
            offer_id=offer_id,
            status=status,
            sort_column=sort_column,
            sort_direction=sort_direction,
            locale=locale
        )

    async def create_products(
            self,
            offer_id: int,
            body: ProductListType | ProductParametr,
            locale: Locale | str = "ru",
    ):
        """
        See Products.create_products
        """
        return await async_handler_api(
            self.client,
            self._create_products,
            None,
            offer_id=offer_id,
            body=body,
            locale=locale
        )

    async def archive_products(
            self,
            offer_id: int,
            product_ids: list[int] | int | None = None,
            locale: Locale | str = "ru",
            delete_all: bool = False,
    ):
        """
        See Products.archive_products
        """
        return await async_handler_api(
            self.client,
            self._archive_products,
            SuccessObject,
            product_ids=product_ids,
            offer_id=offer_id,
            delete_all=delete_all,
            locale=locale
        )

    async def list_splitted_products(
            self,
            offer_id: int,
            variant_id: int,
            status: StatusProduct | str = StatusProduct.IN_STOCK,
            sort_column: str = "created_at",
            sort_direction: OrderDir | str = OrderDir.DESC,
            locale: Locale | str = "ru",
    ):
        """
        See Products.list_splitted_products
        """
        return await async_handler_api(
            self.client,
            self._list_splitted_products,
            ListOfProducts,
            offer_id=offer_id,
            variant_id=variant_id,
            status=status,
            sort_column=sort_column,
            sort_direction=sort_direction,
            locale=locale
        )

    async def create_splitted_products(
            self,
            offer_id: int,
            variant_id: int,
            body: ProductListType | ProductParametr,
            locale: Locale | str = "ru",
    ):
        """
        See Products.create_splitted_products
        """
        return await async_handler_api(
            self.client,
            self._create_splitted_products,
            None,
            offer_id=offer_id,
            variant_id=variant_id,
            body=body,
            locale=locale
        )

    async def archive_splitted_products(
            self,
            offer_id: int,
            variant_id: int,
            product_ids: list[int] | int | None = None,
            locale: Locale | str = "ru",
            delete_all: bool = False,
    ):
        """
        See Products.archive_splitted_products
        """
        return await async_handler_api(
            self.client,
            self._archive_splitted_products,
            SuccessObject,
            offer_id=offer_id,
            variant_id=variant_id,
            product_ids=product_ids,
            delete_all=delete_all,
            locale=locale
        )
