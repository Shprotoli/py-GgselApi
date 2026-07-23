from typing import Any
from json import dumps
from enum import StrEnum
from datetime import datetime

from parameters.globals import Locale
from parameters.api import EnumCrudMethod
from parameters.offers import StatusOffer, SortOffer, DeliveryStatus
from schemas.v2.offer_object import OfferEntity
from api.category import Category, RouteApiV2


class OffersBaseV2(Category, RouteApiV2):
    class BatchAction(StrEnum):
        ACTIVATE = "activate"
        PAUSE = "pause"
        DELETE = "delete"

    def _list_offers(
            self,
            page: int,
            limit: int,
            search: str,
            status: StatusOffer | str,
            sort: SortOffer | str,
            delivery: DeliveryStatus | str,
            updated_at_from: datetime,
            locale: Locale | str,
    ) -> dict[str, Any]:
        params = {
            "page": page,
            "limit": limit,
            "search": search,
            "status": status,
            "sort": sort,
            "delivery": delivery,
            "updated_at_from": updated_at_from,
        }
        headers = {
            "locale": locale,
        }

        return {
            "method": EnumCrudMethod.GET,
            "route": "offers",
            "params": params,
            "headers": headers,
        }

    def _get_offer(
            self,
            id: int,
            locale: Locale | str,
    ) -> dict[str, Any]:
        headers = {
            "locale": locale,
        }

        return {
            "method": EnumCrudMethod.GET,
            "route": f"offers/{id}",
            "headers": headers,
        }

    def _patch_offer(
            self,
            id: int,
            locale: Locale | str,
            body: dict,
    ):
        headers = {
            "locale": locale,
        }

        return {
            "method": EnumCrudMethod.PATCH,
            "route": f"offers/{id}",
            "headers": headers,
            "data": dumps(body)
        }

    def _create_offer(
            self,
            locale: Locale | str,
            body: dict,
    ):
        headers = {
            "locale": locale,
        }

        return {
            "method": EnumCrudMethod.POST,
            "route": f"offers",
            "headers": headers,
            "data": dumps(body)
        }

    def __batch_action_offers(
            self,
            action: BatchAction,
            locale: Locale | str,
            offer_ids: list[int] | int,
    ) -> dict[str, Any]:
        headers = {
            "locale": locale,
        }
        payload = {
            "offer_ids": offer_ids
        }

        return {
            "method": EnumCrudMethod.POST,
            "route": f"offers/batch_{action}",
            "headers": headers,
            "data": dumps(payload)
        }

    def _batch_activate_offers(
            self,
            locale: Locale | str,
            offer_ids: list[int] | int,
    ) -> dict[str, Any]:
        return self.__batch_action_offers(
            action=self.BatchAction.ACTIVATE,
            locale=locale,
            offer_ids=offer_ids,
        )

    def _batch_pause_offers(
            self,
            locale: Locale | str,
            offer_ids: list[int] | int,
    ) -> dict[str, Any]:
        return self.__batch_action_offers(
            action=self.BatchAction.PAUSE,
            locale=locale,
            offer_ids=offer_ids,
        )

    def _batch_delete_offers(
            self,
            locale: Locale | str,
            offer_ids: list[int] | int,
    ) -> dict[str, Any]:
        return self.__batch_action_offers(
            action=self.BatchAction.DELETE,
            locale=locale,
            offer_ids=offer_ids,
        )
