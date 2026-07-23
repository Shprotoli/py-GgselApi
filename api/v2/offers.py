from datetime import datetime

from api.base.offers import OffersBaseV2
from parameters.globals import Locale
from parameters.offers import StatusOffer, SortOffer, DeliveryStatus
from schemas.v2.list_of import ListOfOffers
from schemas.v2.offer_object import OfferObject, OfferEntity
from schemas.general_objects import SuccessObject
from tools.handlers import async_handler_api, handler_api, ApiResult


class Offers(OffersBaseV2):
    def list_offers(
            self,
            search: str,
            delivery: DeliveryStatus | str,
            updated_at_from: datetime,
            page: int = 1,
            limit: int = 100,
            sort: SortOffer | str = SortOffer.PRICE_DESC,
            status: StatusOffer | str = StatusOffer.ACTIVE,
            locale: Locale | str = "ru",
    ) -> ApiResult:
        """
        Source docs: https://seller.ggsel.com/docs/v2/list-offers
        This method returns a list of your products based on the request parameters.
        This is the same as searching on the page - `https://seller.ggsel.com/offers`

        :param search: The line of the part of the title of your product
        :param delivery: The type of delivery that is specified in the product
        :param updated_at_from: The time when the product was updated, no later than which to search
        :param page: Search Page
        :param limit: Limiting the number of products per page
        :param sort: Type of search sorting
        :param status: Product status (active, poused, draft)
        :param locale: Localization response information
        """
        return handler_api(
            self.client,
            self._list_offers,
            ListOfOffers,
            status=status,
            page=page,
            limit=limit,
            search=search,
            sort=sort,
            delivery=delivery,
            updated_at_from=updated_at_from,
            locale=locale
        )

    def get_offer(
            self,
            id: int,
            locale: Locale | str = "ru",
    ) -> ApiResult:
        """
        Source docs: https://seller.ggsel.com/docs/v2/get-offer
        This method returns information about a product by its ID

        :param id: Product ID
        :param locale: Localization response information
        """
        return handler_api(
            self.client,
            self._get_offer,
            OfferObject,
            id=id,
            locale=locale
        )

    def patch_offer(
            self,
            id: int,
            body: OfferEntity | dict,
            locale: Locale | str = "ru",
    ) -> ApiResult:
        """
        Source docs: https://seller.ggsel.com/docs/v2/patch-offer
        Using this method, you can change the parameters of your product by its ID

        :param id: Product ID
        :param body: A dictionary that lists the values to be replaced
                     Example of a car sale change: body={ "is_autoselling": True }
        :param locale: Localization response information
        """
        return handler_api(
            self.client,
            self._patch_offer,
            OfferObject,
            id=id,
            locale=locale,
            body=body,
        )

    def create_offer(
            self,
            body: dict,
            locale: Locale | str = "ru",
    ):
        """
        Source docs: https://seller.ggsel.com/docs/v2/create-offer
        This method allows you to create a product using a dictionary.

        :param body: A dictionary with information for creating a product
        :param locale: Localization response information
        """
        return handler_api(
            self.client,
            self._create_offer,
            OfferObject,
            locale=locale,
            body=body,
        )

    def batch_activate_offers(
            self,
            offer_ids: list[int] | int,
            locale: Locale | str = "ru",
    ) -> ApiResult:
        """
        Source docs: https://seller.ggsel.com/docs/v2/batch-activate-offers
        This method activate a product (or products) by its (or their) ID

        :param offer_ids: Product IDs for the action
        :param locale: Localization response information
        """
        return handler_api(
            self.client,
            self._batch_activate_offers,
            SuccessObject,
            offer_ids=offer_ids,
            locale=locale,
        )

    def batch_pause_offers(
            self,
            offer_ids: list[int] | int,
            locale: Locale | str = "ru",
    ) -> ApiResult:
        """
        Source docs: https://seller.ggsel.com/docs/v2/batch-pause-offers
        This method paused a product (or products) by its (or their) ID

        :param offer_ids: Product IDs for the action
        :param locale: Localization response information
        """
        return handler_api(
            self.client,
            self._batch_pause_offers,
            SuccessObject,
            offer_ids=offer_ids,
            locale=locale,
        )

    def batch_delete_offers(
            self,
            offer_ids: list[int] | int,
            locale: Locale | str = "ru",
    ) -> ApiResult:
        """
        Source docs: https://seller.ggsel.com/docs/v2/batch-delete-offers
        This method deletes a product (or products) by its (or their) ID

        :param offer_ids: Product IDs for the action
        :param locale: Localization response information
        """
        return handler_api(
            self.client,
            self._batch_delete_offers,
            SuccessObject,
            offer_ids=offer_ids,
            locale=locale,
        )


class AsyncOffers(OffersBaseV2):
    async def list_offers(
            self,
            search: str,
            delivery: DeliveryStatus | str,
            updated_at_from: datetime,
            page: int = 1,
            limit: int = 100,
            sort: SortOffer | str = SortOffer.PRICE_DESC,
            status: StatusOffer | str = StatusOffer.ACTIVE,
            locale: Locale | str = "ru",
    ) -> ApiResult:
        """
        See Offers.list_offers
        """
        return await async_handler_api(
            self.client,
            self._list_offers,
            ListOfOffers,
            status=status,
            page=page,
            limit=limit,
            search=search,
            sort=sort,
            delivery=delivery,
            updated_at_from=updated_at_from,
            locale=locale
        )

    async def get_offer(
            self,
            id: int,
            locale: Locale | str = "ru",
    ) -> ApiResult:
        """
        See Offers.get_offer
        """
        return await async_handler_api(
            self.client,
            self._get_offer,
            OfferObject,
            id=id,
            locale=locale
        )

    async def patch_offer(
            self,
            id: int,
            body: OfferEntity | dict,
            locale: Locale | str = "ru",
    ) -> ApiResult:
        """
        See Offers.patch_offer
        """
        return await async_handler_api(
            self.client,
            self._patch_offer,
            OfferObject,
            id=id,
            locale=locale,
            body=body,
        )

    async def create_offer(
            self,
            body: dict,
            locale: Locale | str = "ru",
    ):
        """
        See Offers.create_offer
        """
        return await async_handler_api(
            self.client,
            self._create_offer,
            OfferObject,
            locale=locale,
            body=body,
        )

    async def batch_activate_offers(
            self,
            offer_ids: list[int] | int,
            locale: Locale | str = "ru",
    ) -> ApiResult:
        """
        See Offers.batch_activate_offers
        """
        return await async_handler_api(
            self.client,
            self._batch_activate_offers,
            SuccessObject,
            offer_ids=offer_ids,
            locale=locale,
        )

    async def batch_pause_offers(
            self,
            offer_ids: list[int] | int,
            locale: Locale | str = "ru",
    ) -> ApiResult:
        """
        See Offers.batch_pause_offers
        """
        return await async_handler_api(
            self.client,
            self._batch_pause_offers,
            SuccessObject,
            offer_ids=offer_ids,
            locale=locale,
        )

    async def batch_delete_offers(
            self,
            offer_ids: list[int] | int,
            locale: Locale | str = "ru",
    ) -> ApiResult:
        """
        See Offers.batch_delete_offers
        """
        return await async_handler_api(
            self.client,
            self._batch_delete_offers,
            SuccessObject,
            offer_ids=offer_ids,
            locale=locale,
        )
