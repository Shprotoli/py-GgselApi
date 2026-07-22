from json import dumps
from typing import Any

from api.category import Category, RouteApiV2
from parameters.api import EnumCrudMethod
from parameters.globals import Locale
from parameters.option import OptionList, OptionParametr, OptionListType, OptionValue, OptionValueList, \
    OptionValueListType


class OptionBaseV2(Category, RouteApiV2):
    def _view_option(
            self,
            offer_id: int,
            id: int,
            locale: Locale | str,
    ) -> dict[str, Any]:
        params = {
            "offer_id": offer_id,
            "id": id,
        }
        headers = {
            "locale": locale,
        }

        return {
            "method": EnumCrudMethod.GET,
            "route": f"offers/{offer_id}/options/{id}",
            "params": params,
            "headers": headers,
        }

    def _create_many(
            self,
            offer_id: int,
            body: OptionListType | OptionParametr,
            locale: Locale | str = "ru",
    ) -> dict[str, Any]:
        params = {
            "offer_id": offer_id,
        }
        headers = {
            "locale": locale,
        }

        if isinstance(body, OptionList):
            body = body.asdict()
        elif isinstance(body, OptionParametr):
            body = OptionList([body]).asdict()

        return {
            "method": EnumCrudMethod.POST,
            "route": f"offers/{offer_id}/options",
            "params": params,
            "headers": headers,
            "data": dumps(body),
        }

    def _list_active_offer_options(
            self,
            offer_id: int,
            locale: Locale | str
    ) -> dict[str, Any]:
        params = {
            "offer_id": offer_id,
        }
        headers = {
            "locale": locale,
        }

        return {
            "method": EnumCrudMethod.GET,
            "route": f"offers/{offer_id}/options",
            "params": params,
            "headers": headers,
        }

    def _archive_options(
            self,
            offer_id: int,
            locale: Locale | str,
            options_ids: int | list[int, ...],
            delete_all: bool,
    ) -> dict[str, Any]:
        params = {
            "offer_id": offer_id,
        }
        headers = {
            "locale": locale,
        }
        payloads = {
            "options_ids": options_ids,
            "delete_all": str(delete_all).lower()
        }

        return {
            "method": EnumCrudMethod.DELETE,
            "route": f"offers/{offer_id}/options",
            "params": params,
            "headers": headers,
            "data": dumps(payloads),
        }

    def _create_or_update_variants(
            self,
            offer_id: int,
            option_id: int,
            locale: Locale | str,
            body: OptionValue | OptionValueListType,
    ) -> dict[str, Any]:
        params = {
            "offer_id": offer_id,
            "option_id": option_id,
        }
        headers = {
            "locale": locale,
        }

        if isinstance(body, OptionValueList):
            body = body.asdict()
        elif isinstance(body, OptionValue):
            body = OptionValueList([body]).asdict()

        return {
            "method": EnumCrudMethod.POST,
            "route": f"offers/{offer_id}/options/{option_id}/variants",
            "params": params,
            "headers": headers,
            "data": dumps(body),
        }

    def _archive_option_variants_asynchronously(
            self,
            offer_id: int,
            option_id: int,
            locale: Locale | str,
            option_variant_ids: list[int] | int,
            delete_all: bool
    ):
        params = {
            "offer_id": offer_id,
            "option_id": option_id,
        }
        headers = {
            "locale": locale,
        }
        payloads = {
            "option_variant_ids": option_variant_ids,
            "delete_all": str(delete_all).lower()
        }

        return {
            "method": EnumCrudMethod.DELETE,
            "route": f"offers/{offer_id}/options/{option_id}/variants",
            "params": params,
            "headers": headers,
            "data": dumps(payloads),
        }
