from parameters.globals import Locale

from tools.handlers import handler_response_api, ApiResult
from api.base.categories import CategoriesBaseV2
from schemas.v2.list_of import ListOfCategories


class Categories(CategoriesBaseV2):
    def list_of_categories(
            self,
            parent_id: int,
            page: int = 1,
            limit: int = 10,
            locale: str | Locale = "ru"
    ) -> ApiResult:
        """
        Source docs: https://seller.ggsel.com/docs/v2/list-of-categories
        This method returns information about the category.
        This includes the name, the category's commission rate, and more...

        :param parent_id: ID category
        :param page: Count page category
        :param limit: Count category
        :param locale: Localization response information
        """
        response = self.client.get(**self._list_of_categories(parent_id, page, limit, locale))
        data = response.json()

        return handler_response_api(ListOfCategories, data=data)

    def search_categories(
            self,
            q: str,
            page: int = 1,
            limit: int = 10,
            locale: str | Locale = "ru",
    ) -> ApiResult:
        """
        Source docs: https://seller.ggsel.com/docs/v2/search-categories
        This method works like a "search" on GGSel by category

        :param q: Your request
        :param page: Count page category
        :param limit: Count category
        :param locale: Localization response information
        """
        response = self.client.get(**self._search_categories(page, limit, q, locale))
        data = response.json()

        return handler_response_api(ListOfCategories, data=data)


class AsyncCategories(CategoriesBaseV2):
    async def list_of_categories(
            self,
            parent_id: int,
            page: int = 1,
            limit: int = 10,
            locale: str | Locale = "ru"
    ) -> ApiResult:
        """
        See v2.Categories.list_of_categories
        """
        response = await self.client.get(**self._list_of_categories(parent_id, page, limit, locale))
        data = response.json()

        return handler_response_api(ListOfCategories, data=data)

    async def search_categories(
            self,
            q: str,
            page: int = 1,
            limit: int = 10,
            locale: str | Locale = "ru",
    ) -> ApiResult:
        """
        See v2.Categories.search_categories
        """
        response = await self.client.get(**self._search_categories(page, limit, q, locale))
        data = response.json()

        return handler_response_api(ListOfCategories, data=data)
