from parameters.globals import Locale

from tools.handlers import handler_response_api, ApiResult
from api.base.categories import CategoriesBaseV2
from schemas.v2.list_of import ListOfCategories


class Categories(CategoriesBaseV2):
    def list_of_categories(
            self,
            parent_id: int,
            page: int,
            limit: int,
            locale: Locale = "ru"
    ) -> ApiResult:
        """

        :param parent_id:
        :param page:
        :param limit:
        :param locale:
        :return:
        """
        response = self.client.get(**self._list_of_categories(parent_id, page, limit, locale))
        data = response.json()

        return handler_response_api(ListOfCategories, data=data)


class AsyncCategories(CategoriesBaseV2):
    def list_of_categories(
            self,
            parent_id: int,
            page: int,
            limit: int,
            locale: Locale = "ru"
    ) -> ApiResult:
        pass