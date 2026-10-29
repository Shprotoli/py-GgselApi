# Requests of the `Offers` group of the GGSel API V2
from datetime import datetime

from ggsel_py.api.category import (
    Category, AsyncCategory, RouteApiV2, RequestSpec, build_request, endpoint, locale_header,
)
from ggsel_py.parameters.api import EnumCrudMethod
from ggsel_py.parameters.globals import Locale
from ggsel_py.parameters.offers import StatusOffer, SortOffer, DeliveryStatus, BatchAction
from ggsel_py.schemas.general_objects import SuccessObject
from ggsel_py.schemas.v2.list_of import ListOfOffers
from ggsel_py.schemas.v2.offer_object import OfferObject, OfferEntity


class OffersEndpointsV2(Category, RouteApiV2):
    BatchAction = BatchAction

    @endpoint(ListOfOffers)
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
    ) -> RequestSpec:
        """
        Source docs: https://seller.ggsel.com/docs/v2/list-offers
        This method returns a list of your products based on the request parameters.
        This is the same as searching on the page - `https://seller.ggsel.com/offers`

        :param search: The line of the part of the title of your product
        :param delivery: The type of delivery that is specified in the product
        :param updated_at_from: The time when the product was updated, no later than which to search
        """
        params = {
            "page": page,
            "limit": limit,
            "search": search,
            "status": status,
            "sort": sort,
            "delivery": delivery,
            "updated_at_from": updated_at_from,
        }

        return build_request(EnumCrudMethod.GET, "offers", params=params, headers=locale_header(locale))

    @endpoint(OfferObject)
    def get_offer(
            self,
            id: int,
            locale: Locale | str = "ru",
    ) -> RequestSpec:
        """
        Source docs: https://seller.ggsel.com/docs/v2/get-offer
        """
        return build_request(EnumCrudMethod.GET, f"offers/{id}", headers=locale_header(locale))

    @endpoint(OfferObject)
    def patch_offer(
            self,
            id: int,
            body: OfferEntity | dict,
            locale: Locale | str = "ru",
    ) -> RequestSpec:
        """
        Source docs: https://seller.ggsel.com/docs/v2/patch-offer
        Changes the parameters of your product by its ID

        :param body: A dictionary that lists the values to be replaced
                     Example of a car sale change: body={ "is_autoselling": True }
        """
        return build_request(EnumCrudMethod.PATCH, f"offers/{id}", headers=locale_header(locale), payload=body)

    @endpoint(OfferObject)
    def create_offer(
            self,
            body: dict,
            locale: Locale | str = "ru",
    ) -> RequestSpec:
        """
        Source docs: https://seller.ggsel.com/docs/v2/create-offer
        Creates a product from a dictionary (see the templates in `ggsel_py.parameters.offers`)
        """
        return build_request(EnumCrudMethod.POST, "offers", headers=locale_header(locale), payload=body)

    def _batch_action(
            self,
            action: BatchAction,
            offer_ids: list[int] | int,
            locale: Locale | str,
    ) -> RequestSpec:
        return build_request(
            EnumCrudMethod.POST,
            f"offers/batch_{action}",
            headers=locale_header(locale),
            payload={"offer_ids": offer_ids},
        )

    @endpoint(SuccessObject)
    def batch_activate_offers(
            self,
            offer_ids: list[int] | int,
            locale: Locale | str = "ru",
    ) -> RequestSpec:
        """
        Source docs: https://seller.ggsel.com/docs/v2/batch-activate-offers
        """
        return self._batch_action(BatchAction.ACTIVATE, offer_ids, locale)

    @endpoint(SuccessObject)
    def batch_pause_offers(
            self,
            offer_ids: list[int] | int,
            locale: Locale | str = "ru",
    ) -> RequestSpec:
        """
        Source docs: https://seller.ggsel.com/docs/v2/batch-pause-offers
        """
        return self._batch_action(BatchAction.PAUSE, offer_ids, locale)

    @endpoint(SuccessObject)
    def batch_delete_offers(
            self,
            offer_ids: list[int] | int,
            locale: Locale | str = "ru",
    ) -> RequestSpec:
        """
        Source docs: https://seller.ggsel.com/docs/v2/batch-delete-offers
        """
        return self._batch_action(BatchAction.DELETE, offer_ids, locale)


class Offers(OffersEndpointsV2):
    pass


class AsyncOffers(AsyncCategory, OffersEndpointsV2):
    pass
