from typing import Any

from parameters.globals import Lang
from api.category import Category


class CategoriesBaseV1(Category):
    ROUTE = "api_sellers/api"

    def _all_categories(
            self,
            page: int = 1,
            count: int = 10,
            category_id: str = "",
            lang: str | Lang = "ru-RU",
    ) -> dict[str, Any]:
        params = {
            "page": page,
            "count": count,
            "category_id": category_id,
        }
        headers = {
            "lang": lang,
        }

        return {
            "route": "categories",
            "params": params,
            "headers": headers,
        }


class CategoriesBaseV2(Category):
    ROUTE = "api_sellers/v2"
