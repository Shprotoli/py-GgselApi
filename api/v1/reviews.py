from tools.handlers import handler_response_api, ApiResult
from parameters.reviews import TypeReview
from parameters.globals import Lang
from schemas.reviews_object import ReviewsObject
from api.v1.category import Category


class Reviews(Category):
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
        params = {
            "product_id": product_id,
            "page": page,
            "count": count,
            "type": type,
        }
        headers = {
            "locale": locale,
        }

        response = self.client.get("reviews", params=params, headers=headers)
        data = response.json()

        return handler_response_api(ReviewsObject, data=data)

