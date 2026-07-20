# A class file that handles requests from the `Categories` category of the GGSell API
from tools.handlers import handler_api, async_handler_api, EnumMethodHandle, ApiResult
from parameters.globals import Lang
from schemas.v1.categories_object import CategoriesObject
from api.base.categories import CategoriesBaseV1 as CategoriesBase


class Categories(CategoriesBase):
    def all_categories(
            self,
            page: int = 1,
            count: int = 10,
            category_id: str = "",
            lang: str | Lang = "ru-RU",
    ) -> ApiResult:
        """
        Source docs: https://seller.ggsel.com/docs/return-all-categories
        This feature allows you to receive lists of GGSel categories/subcategories

        :param page: Category page
        :param count: The number of master categories that will be found
        :param category_id: The ID of the specific category to be found
                            (P.S In this case, count will affect the categories within the requested category)
        :param lang: The language in which the categories will be returned
        :return: dataclass CategoriesObject containing a json response from the API
        """
        return handler_api(
            EnumMethodHandle.GET,
            self.client,
            self._all_categories,
            CategoriesObject,
            page=page,
            count=count,
            category_id=category_id,
            lang=lang
        )


class AsyncCategories(CategoriesBase):
    async def all_categories(
            self,
            page: int = 1,
            count: int = 10,
            category_id: str = "",
            lang: str | Lang = "ru-RU",
    ) -> ApiResult:
        """
        See Categories.all_categories
        """
        return await async_handler_api(
            EnumMethodHandle.GET,
            self.client,
            self._all_categories,
            CategoriesObject,
            page=page,
            count=count,
            category_id=category_id,
            lang=lang
        )
