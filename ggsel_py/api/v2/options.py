# Requests of the `Options` group of the GGSel API V2
from ggsel_py.api.category import (
    Category, AsyncCategory, RouteApiV2, RequestSpec, build_request, endpoint, locale_header,
)
from ggsel_py.parameters.api import EnumCrudMethod
from ggsel_py.parameters.common import archive_payload, as_request_body
from ggsel_py.parameters.globals import Locale
from ggsel_py.parameters.options import (
    OptionList,
    OptionParametr,
    OptionListType,
    OptionValue,
    OptionValueList,
    OptionValueListType,
    VisibilityItem,
)
from ggsel_py.schemas.general_objects import SuccessObject
from ggsel_py.schemas.v2.list_of import ListOfOption
from ggsel_py.schemas.v2.option_object import OptionObject, VariantObject


def visibility_payload(items_field: str, items: list[VisibilityItem | dict]) -> dict:
    return {
        items_field: [
            {"id": item.id, "status": str(item.status)} if isinstance(item, VisibilityItem) else item
            for item in items
        ],
    }


class OptionEndpointsV2(Category, RouteApiV2):
    @endpoint(OptionObject)
    def view_option(
            self,
            offer_id: int,
            id: int,
            locale: Locale | str = "ru",
    ) -> RequestSpec:
        """
        Source docs: https://seller.ggsel.com/docs/v2/view-option
        This method returns a list of options by parameter ID and product ID.

        Example: There is a "Subscription period" parameter with ID `3095078` for a product with ID `102238374`,
        then by executing the following code: option_api_category.view_option(102238374, 3095078)
        You will receive a list of options (or sub-parameters)

        :param id: ID of the parameter (not the option!) of the product
        """
        params = {
            "offer_id": offer_id,
            "id": id,
        }

        return build_request(
            EnumCrudMethod.GET,
            f"offers/{offer_id}/options/{id}",
            params=params,
            headers=locale_header(locale),
        )

    @endpoint(OptionObject)
    def create_many(
            self,
            offer_id: int,
            body: OptionListType | OptionParametr,
            locale: Locale | str = "ru",
    ) -> RequestSpec:
        """
        Source docs: https://seller.ggsel.com/docs/v2/create-many
        This method creates a option for a specific product by ID

        :param body: Information about the option.
                     Use `OptionParametr` or `OptionList` for your convenience.
                     You can also set the option type using the enum - `OptionVariant`
        """
        return build_request(
            EnumCrudMethod.POST,
            f"offers/{offer_id}/options",
            params={"offer_id": offer_id},
            headers=locale_header(locale),
            payload=as_request_body(body, OptionList, OptionParametr),
        )

    @endpoint(ListOfOption)
    def list_active_offer_options(
            self,
            offer_id: int,
            locale: Locale | str = "ru",
    ) -> RequestSpec:
        """
        Source docs: https://seller.ggsel.com/docs/v2/list-offer-options-visible-to-seller
        This method retrieves a list of options by product ID. Unlike `view_option`, this method returns
        a list of all parameters (and their variants) instead of a list of options.
        """
        return build_request(
            EnumCrudMethod.GET,
            f"offers/{offer_id}/options",
            params={"offer_id": offer_id},
            headers=locale_header(locale),
        )

    @endpoint(SuccessObject)
    def archive_options(
            self,
            offer_id: int,
            options_ids: int | list[int] | None = None,
            locale: Locale | str = "ru",
            delete_all: bool = False,
    ) -> RequestSpec:
        """
        Source docs: https://seller.ggsel.com/docs/v2/archive-options
        This method removes an option or options from a given product by a given option id
        """
        return build_request(
            EnumCrudMethod.DELETE,
            f"offers/{offer_id}/options",
            params={"offer_id": offer_id},
            headers=locale_header(locale),
            payload=archive_payload("options_ids", options_ids, delete_all),
        )

    @endpoint(None)
    def batch_update_options_visibility(
            self,
            offer_id: int,
            options: list[VisibilityItem | dict],
            locale: Locale | str = "ru",
    ) -> RequestSpec:
        """
        Source docs: https://seller.ggsel.com/docs/v2/batch-update-options-visibility
        Shows or hides options of a product

        :param options: `VisibilityItem(id=..., status=VisibilityStatus.HIDDEN)` or `{"id": ..., "status": ...}`
        """
        return build_request(
            EnumCrudMethod.PATCH,
            f"offers/{offer_id}/options/batch_visibility",
            headers=locale_header(locale),
            payload=visibility_payload("options", options),
        )

    @endpoint(VariantObject)
    def create_or_update_variants(
            self,
            offer_id: int,
            option_id: int,
            body: OptionValue | OptionValueListType,
            locale: Locale | str = "ru",
    ) -> RequestSpec:
        """
        Source docs: https://seller.ggsel.com/docs/v2/create-or-update-variants
        This method creates options for the option by product ID and option ID

        :param body: Information about the option.
                     Use `OptionValue` or `OptionValueList` for your convenience.
                     You can also set the option settings using the enum - `ImpactType` and `DiscountType`
        """
        params = {
            "offer_id": offer_id,
            "option_id": option_id,
        }

        return build_request(
            EnumCrudMethod.POST,
            f"offers/{offer_id}/options/{option_id}/variants",
            params=params,
            headers=locale_header(locale),
            payload=as_request_body(body, OptionValueList, OptionValue),
        )

    @endpoint(SuccessObject)
    def archive_option_variants_asynchronously(
            self,
            offer_id: int,
            option_id: int,
            option_variant_ids: list[int] | int | None = None,
            locale: Locale | str = "ru",
            delete_all: bool = False,
    ) -> RequestSpec:
        """
        Source docs: https://seller.ggsel.com/docs/v2/archive-option-variants-asynchronously
        This method creates an asynchronous task to remove variants from an option.
        The result of the task can be obtained with `async_jobs.get_async_job_result`.

        :param option_variant_ids: ID Variant or a list of ID Variant. If you want to delete all variants,
                                   pass None and pass True in `delete_all`
        :param delete_all: `True` or `False` to remove all variants from option.
                           Only works if option_variant_ids is set to `None`
        """
        params = {
            "offer_id": offer_id,
            "option_id": option_id,
        }

        return build_request(
            EnumCrudMethod.DELETE,
            f"offers/{offer_id}/options/{option_id}/variants",
            params=params,
            headers=locale_header(locale),
            payload=archive_payload("option_variant_ids", option_variant_ids, delete_all),
        )

    @endpoint(None)
    def batch_update_variants_visibility(
            self,
            offer_id: int,
            option_id: int,
            variants: list[VisibilityItem | dict],
            locale: Locale | str = "ru",
    ) -> RequestSpec:
        """
        Source docs: https://seller.ggsel.com/docs/v2/batch-update-variants-visibility
        Shows or hides variants of an option

        :param variants: `VisibilityItem(id=..., status=VisibilityStatus.HIDDEN)` or `{"id": ..., "status": ...}`
        """
        return build_request(
            EnumCrudMethod.PATCH,
            f"offers/{offer_id}/options/{option_id}/variants/batch_visibility",
            headers=locale_header(locale),
            payload=visibility_payload("variants", variants),
        )


class Option(OptionEndpointsV2):
    pass


class AsyncOption(AsyncCategory, OptionEndpointsV2):
    pass
