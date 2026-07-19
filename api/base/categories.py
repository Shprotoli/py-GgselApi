from typing import Any

from parameters.globals import Lang, Locale
from api.category import Category, RouteApiV1, RouteApiV2


class CategoriesBaseV1(Category, RouteApiV1):
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


class CategoriesBaseV2(Category, RouteApiV2):
    def _list_of_categories(
            self,
            parent_id: int,
            page: int,
            limit: int,
            locale: str | Locale = "ru",
    ) -> dict[str, Any]:
        params = {
            "parent_id": parent_id,
            "page": page,
            "limit": limit,
        }
        headers = {
            "locale": locale,
        }

        return {
            "route": "categories",
            "params": params,
            "headers": headers,
        }
