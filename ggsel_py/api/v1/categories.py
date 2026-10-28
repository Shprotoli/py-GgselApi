# Requests of the `Categories` category of the GGSel API
from ggsel_py.api.category import Category, AsyncCategory, RouteApiV1, RequestSpec, build_request, endpoint
from ggsel_py.parameters.api import EnumCrudMethod, Header
from ggsel_py.parameters.globals import Lang
from ggsel_py.schemas.v1.categories_object import CategoriesObject


class CategoriesEndpointsV1(Category, RouteApiV1):
    @endpoint(CategoriesObject)
    def all_categories(
            self,
            page: int = 1,
            count: int = 10,
            category_id: str = "",
            lang: str | Lang = "ru-RU",
    ) -> RequestSpec:
        """
        Source docs: https://seller.ggsel.com/docs/return-all-categories
        Returns lists of GGSel categories/subcategories

        :param count: The number of master categories that will be found
        :param category_id: The ID of the specific category to be found
                            (P.S In this case, count will affect the categories within the requested category)
        """
        params = {
            "page": page,
            "count": count,
            "category_id": category_id,
        }

        return build_request(EnumCrudMethod.GET, "categories", params=params, headers={Header.LANG: str(lang)})


class Categories(CategoriesEndpointsV1):
    pass


class AsyncCategories(AsyncCategory, CategoriesEndpointsV1):
    pass
