from typing import Any

from api.category import Category, RouteApiV1
from parameters.reviews import TypeReview
from parameters.globals import Lang


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
            "route": "reviews",
            "params": params,
            "headers": headers,
        }
