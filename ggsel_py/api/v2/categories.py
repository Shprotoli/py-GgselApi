# Requests of the `Category` group of the GGSel API V2
from ggsel_py.api.category import (
    Category, AsyncCategory, RouteApiV2, RequestSpec, build_request, endpoint, locale_header,
)
from ggsel_py.parameters.api import EnumCrudMethod
from ggsel_py.parameters.globals import Locale
from ggsel_py.schemas.v2.list_of import ListOfCategories


class CategoriesEndpointsV2(Category, RouteApiV2):
    @endpoint(ListOfCategories)
    def list_of_categories(
            self,
            parent_id: int,
            page: int = 1,
            limit: int = 10,
            locale: str | Locale = "ru"
    ) -> RequestSpec:
        """
        Source docs: https://seller.ggsel.com/docs/v2/list-of-categories
        This method returns information about the category.
        This includes the name, the category's commission rate, and more...
        """
        params = {
            "parent_id": parent_id,
            "page": page,
            "limit": limit,
        }

        return build_request(EnumCrudMethod.GET, "categories", params=params, headers=locale_header(locale))

    @endpoint(ListOfCategories)
    def search_categories(
            self,
            q: str,
            page: int = 1,
            limit: int = 10,
            locale: str | Locale = "ru",
    ) -> RequestSpec:
        """
        Source docs: https://seller.ggsel.com/docs/v2/search-categories
        This method works like a "search" on GGSel by category

        :param q: Your request
        """
        params = {
            "page": page,
            "limit": limit,
            "q": q,
        }

        return build_request(EnumCrudMethod.GET, "categories/search", params=params, headers=locale_header(locale))


class Categories(CategoriesEndpointsV2):
    pass


class AsyncCategories(AsyncCategory, CategoriesEndpointsV2):
    pass
