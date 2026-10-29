# Requests of the `Products` group of the GGSel API V2 (the content of offers)
from ggsel_py.api.category import (
    Category, AsyncCategory, RouteApiV2, RequestSpec, build_request, endpoint, locale_header,
)
from ggsel_py.parameters.api import EnumCrudMethod
from ggsel_py.parameters.common import archive_payload, as_request_body
from ggsel_py.parameters.globals import Locale
from ggsel_py.parameters.products import StatusProduct, OrderDir, ProductList, ProductParametr, ProductListType
from ggsel_py.schemas.general_objects import SuccessObject
from ggsel_py.schemas.v2.list_of import ListOfProducts


def sort_params(status: StatusProduct | str, sort_column: str, sort_direction: OrderDir | str) -> dict:
    return {
        "status": status,
        "sort_column": sort_column,
        "sort_direction": sort_direction,
    }


class ProductsEndpointsV2(Category, RouteApiV2):
    @endpoint(ListOfProducts)
    def list_products(
            self,
            offer_id: int,
            status: StatusProduct | str = StatusProduct.IN_STOCK,
            sort_column: str = "created_at",
            sort_direction: OrderDir | str = OrderDir.DESC,
            locale: Locale | str = "ru",
    ) -> RequestSpec:
        """
        Source docs: https://seller.ggsel.com/docs/v2/list-products
        This method returns a list of items added to the product.
        """
        return build_request(
            EnumCrudMethod.GET,
            f"offers/{offer_id}/products",
            params=sort_params(status, sort_column, sort_direction),
            headers=locale_header(locale),
        )

    @endpoint(None)
    def create_products(
            self,
            offer_id: int,
            body: ProductListType | ProductParametr,
            locale: Locale | str = "ru",
    ) -> RequestSpec:
        """
        Source docs: https://seller.ggsel.com/docs/v2/create-products
        Adds content to a product
        """
        return build_request(
            EnumCrudMethod.POST,
            f"offers/{offer_id}/products",
            params={"offer_id": offer_id},
            headers=locale_header(locale),
            payload=as_request_body(body, ProductList, ProductParametr),
        )

    @endpoint(SuccessObject)
    def archive_products(
            self,
            offer_id: int,
            product_ids: list[int] | int | None = None,
            locale: Locale | str = "ru",
            delete_all: bool = False,
    ) -> RequestSpec:
        """
        Source docs: https://seller.ggsel.com/docs/v2/archive-products

        :param product_ids: The ID of the product (or a list of product IDs) that you want to delete.
                            You can find the current product IDs using the `list_products` method
        :param delete_all: Should I delete all the products - True or False.
                           If you want to delete all products, you should not pass anything (or pass `None`) in the `product_ids` field
        """
        return build_request(
            EnumCrudMethod.DELETE,
            f"offers/{offer_id}/products",
            params={"offer_id": offer_id},
            headers=locale_header(locale),
            payload=archive_payload("product_ids", product_ids, delete_all),
        )

    @endpoint(ListOfProducts)
    def list_splitted_products(
            self,
            offer_id: int,
            variant_id: int,
            status: StatusProduct | str = StatusProduct.IN_STOCK,
            sort_column: str = "created_at",
            sort_direction: OrderDir | str = OrderDir.DESC,
            locale: Locale | str = "ru",
    ) -> RequestSpec:
        """
        Source docs: https://seller.ggsel.com/docs/v2/list-splitted-products
        This method returns the product content for splitted products by product ID and variant ID
        """
        return build_request(
            EnumCrudMethod.GET,
            f"offers/{offer_id}/variants/{variant_id}/splitted_products",
            params=sort_params(status, sort_column, sort_direction),
            headers=locale_header(locale),
        )

    @endpoint(None)
    def create_splitted_products(
            self,
            offer_id: int,
            variant_id: int,
            body: ProductListType | ProductParametr,
            locale: Locale | str = "ru",
    ) -> RequestSpec:
        """
        Source docs: https://seller.ggsel.com/docs/v2/create-splitted-products
        This method adds the product content to a specific variant using the product ID and variant ID.
        """
        params = {
            "offer_id": offer_id,
            "variant_id": variant_id,
        }

        return build_request(
            EnumCrudMethod.POST,
            f"offers/{offer_id}/variants/{variant_id}/splitted_products",
            params=params,
            headers=locale_header(locale),
            payload=as_request_body(body, ProductList, ProductParametr),
        )

    @endpoint(SuccessObject)
    def archive_splitted_products(
            self,
            offer_id: int,
            variant_id: int,
            product_ids: list[int] | int | None = None,
            locale: Locale | str = "ru",
            delete_all: bool = False,
    ) -> RequestSpec:
        """
        Source docs: https://seller.ggsel.com/docs/v2/archive-splitted-products
        Removes a product (or products) by lot ID (`offer_id`), variant ID (`variant_id`), and product ID (`products_ids`)

        :param delete_all: Should I delete all the products - True or False.
                           If you want to delete all products, you should not pass anything (or pass `None`) in the `product_ids` field
        """
        params = {
            "offer_id": offer_id,
            "variant_id": variant_id,
        }

        return build_request(
            EnumCrudMethod.DELETE,
            f"offers/{offer_id}/variants/{variant_id}/splitted_products",
            params=params,
            headers=locale_header(locale),
            payload=archive_payload("product_ids", product_ids, delete_all),
        )


class Products(ProductsEndpointsV2):
    pass


class AsyncProducts(AsyncCategory, ProductsEndpointsV2):
    pass
