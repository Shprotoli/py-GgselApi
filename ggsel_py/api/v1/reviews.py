# Requests of the `Reviews` category of the GGSel API
from ggsel_py.api.category import (
    Category, AsyncCategory, RouteApiV1, RequestSpec, build_request, endpoint, locale_header,
)
from ggsel_py.parameters.api import EnumCrudMethod
from ggsel_py.parameters.globals import Lang
from ggsel_py.parameters.reviews import TypeReview
from ggsel_py.schemas.v1.reviews_object import ReviewsObject


class ReviewsEndpointsV1(Category, RouteApiV1):
    @endpoint(ReviewsObject)
    def user_reviews(
            self,
            product_id: int,
            type: str | TypeReview = TypeReview.ALL,
            page: int = 1,
            count: int = 10,
            locale: str | Lang = Lang.RU
    ) -> RequestSpec:
        """
        Source docs: https://seller.ggsel.com/docs/return-user-reviews
        Returns a list of reviews for the requested product
        """
        params = {
            "product_id": product_id,
            "page": page,
            "count": count,
            "type": type,
        }

        return build_request(EnumCrudMethod.GET, "reviews", params=params, headers=locale_header(locale))


class Reviews(ReviewsEndpointsV1):
    pass


class AsyncReviews(AsyncCategory, ReviewsEndpointsV1):
    pass
