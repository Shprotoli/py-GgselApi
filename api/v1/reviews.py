from tools.handlers import handler_api, async_handler_api, ApiResult
from parameters.reviews import TypeReview
from parameters.globals import Lang
from schemas.v1.reviews_object import ReviewsObject
from api.base.reviews import ReviewsBaseV1


class Reviews(ReviewsBaseV1):
    def user_reviews(
            self,
            product_id: int,
            type: str | TypeReview = TypeReview.ALL,
            page: int = 1,
            count: int = 10,
            locale: str | Lang = Lang.RU
    ) -> ApiResult:
        """
        Source docs: https://seller.ggsel.com/docs/return-user-reviews
        This method returns a list of reviews for the requested product

        :param type: Type of review
        :param product_id: The unique product ID for which you want to get a list of reviews
        :param page: Page number (pagination)
        :param count: How many items can be returned per request (limit)
        :param locale: API Response Language
        :return:
        """
        return handler_api(
            self.client,
            self._user_reviews,
            ReviewsObject,
            product_id=product_id,
            type=type,
            page=page,
            count=count,
            locale=locale
        )


class AsyncReviews(ReviewsBaseV1):
    async def user_reviews(
            self,
            product_id: int,
            type: str | TypeReview = TypeReview.ALL,
            page: int = 1,
            count: int = 10,
            locale: str | Lang = Lang.RU
    ) -> ApiResult:
        """
        See Reviews.user_reviews
        """
        return await async_handler_api(
            self.client,
            self._user_reviews,
            ReviewsObject,
            product_id=product_id,
            type=type,
            page=page,
            count=count,
            locale=locale
        )
