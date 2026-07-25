from typing import Any

from ggsel_py.api.category import Category, RouteApiV1
from ggsel_py.parameters.reviews import TypeReview
from ggsel_py.parameters.api import EnumCrudMethod
from ggsel_py.parameters.globals import Lang


class ReviewsBaseV1(Category, RouteApiV1):
    def _user_reviews(
            self,
            product_id: int,
            type: str | TypeReview = TypeReview.ALL,
            page: int = 1,
            count: int = 10,
            locale: str | Lang = Lang.RU
    ) -> dict[str, Any]:
        params = {
            "product_id": product_id,
            "page": page,
            "count": count,
            "type": type,
        }
        headers = {
            "locale": str(locale),
        }

        return {
            "method": EnumCrudMethod.GET,
            "route": "reviews",
            "params": params,
            "headers": headers,
        }
