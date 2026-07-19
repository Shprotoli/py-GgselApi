from parameters.globals import Lang

from tools.handlers import handler_response_api, ApiResult
from api.base.categories import CategoriesBaseV2


class Categories(CategoriesBaseV2):
    def list_of_categories(
            self,
            parent_id: int,
            page: int,
            limit: int,
            locale: Lang = "ru-RU"
    ) -> ApiResult:
        pass


class AsyncCategories(CategoriesBaseV2):
    def list_of_categories(
            self,
            parent_id: int,
            page: int,
            limit: int,
            locale: Lang = "ru-RU"
    ) -> ApiResult:
        pass