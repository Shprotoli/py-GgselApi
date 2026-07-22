from api.base.options import OptionBaseV2
from tools.handlers import handler_api, async_handler_api, ApiResult
from schemas.v2.option_object import OptionObject, SuccessObject, OptionValueObject
from parameters.globals import Locale
from parameters.options import OptionParametr, OptionListType, OptionValue, OptionValueListType


class Option(OptionBaseV2):
    def view_option(
            self,
            offer_id: int,
            id: int,
            locale: Locale | str = "ru",
    ) -> ApiResult:
        """
        Source docs: https://seller.ggsel.com/docs/v2/view-option
        This method returns a list of options by parameter ID and product ID.

        Example: There is a "Subscription period" parameter with ID `3095078` for a product with ID `102238374`,
        then by executing the following code: option_api_category.view_option(102238374, 3095078)
        You will receive a list of options (or sub-parameters)

        :param offer_id: Product ID
        :param id: ID of the parameter (not the option!) of the product
        :param locale: Response language
        """
        return handler_api(
            self.client,
            self._view_option,
            OptionObject,
            offer_id=offer_id,
            id=id,
            locale=locale,
        )

    def create_many(
            self,
            offer_id: int,
            body: OptionListType | OptionParametr,
            locale: Locale | str = "ru",
    ) -> ApiResult:
        """
        Source docs: https://seller.ggsel.com/docs/v2/create-many
        This method creates a option for a specific product by ID

        :param offer_id: Product ID
        :param body: Information about the option.
                     Use `OptionParametr` or `OptionList` for your convenience.
                     You can also set the option type using the enum - `OptionVariant`
        :param locale: Response language
        """
        return handler_api(
            self.client,
            self._create_many,
            OptionObject,
            offer_id=offer_id,
            body=body,
            locale=locale,
        )

    def list_active_offer_options(
            self,
            offer_id: int,
            locale: Locale | str = "ru",
    ) -> ApiResult:
        """
        Source docs: https://seller.ggsel.com/docs/v2/list-active-offer-options
        This method retrieves a list of options by product ID. Unlike `view_option`, this method returns
        a list of all parameters (and their variants) instead of a list of options.

        :param offer_id: Product ID
        :param locale: Response language
        """
        return handler_api(
            self.client,
            self._list_active_offer_options,
            OptionObject,
            offer_id=offer_id,
            locale=locale,
        )

    def archive_options(
            self,
            offer_id: int,
            options_ids: int | list[int],
            locale: Locale | str = "ru",
            delete_all: bool = False,
    ) -> ApiResult:
        """
        Source docs: https://seller.ggsel.com/docs/v2/archive-options
        This method removes an option or options from a given product by a given option id

        :param offer_id: Product ID
        :param options_ids: ID or list of ID options
        :param locale: Response language
        :param delete_all: Delete all options
        """
        return handler_api(
            self.client,
            self._archive_options,
            SuccessObject,
            offer_id=offer_id,
            locale=locale,
            options_ids=options_ids,
            delete_all=delete_all,
        )

    def create_or_update_variants(
            self,
            offer_id: int,
            option_id: int,
            body: OptionValue | OptionValueListType,
            locale: Locale | str = "ru",
    ) -> ApiResult:
        """
        Source docs: https://seller.ggsel.com/docs/v2/create-or-update-variants
        This method creates options for the option by product ID and option ID

        :param offer_id: Product ID
        :param option_id: ID option for add/update variants
        :param body: Information about the option.
                     Use `OptionValue` or `OptionValueList` for your convenience.
                     You can also set the option settings using the enum - `ImpactType` and `DiscountType`
        :param locale: Response language
        """
        return handler_api(
            self.client,
            self._create_or_update_variants,
            OptionValueObject,
            offer_id=offer_id,
            locale=locale,
            option_id=option_id,
            body=body,
        )

    def archive_option_variants_asynchronously(
            self,
            offer_id: int,
            option_id: int,
            option_variant_ids: list[int] | int | None,
            locale: Locale | str = "ru",
            delete_all: bool = False,
    ):
        """
        Source docs: https://seller.ggsel.com/docs/v2/archive-option-variants-asynchronously
        This method creates an asynchronous task to remove variants from an option

        :param offer_id: Product ID
        :param option_id: ID option
        :param option_variant_ids: ID Variant or a list of ID Variant. If you want to delete all variants,
                                   pass None and pass True in `delete_all`
        :param locale: Response language
        :param delete_all: `True` or `False` to remove all variants from option.
                           Only works if option_variant_ids is set to `None`
        """
        return handler_api(
            self.client,
            self._archive_option_variants_asynchronously,
            SuccessObject,
            offer_id=offer_id,
            locale=locale,
            option_id=option_id,
            option_variant_ids=option_variant_ids,
            delete_all=delete_all,
        )


class AsyncOption(OptionBaseV2):
    async def view_option(
            self,
            offer_id: int,
            id: int,
            locale: Locale | str = "ru",
    ) -> ApiResult:
        """
        See Option.view_option
        """
        return await async_handler_api(
            self.client,
            self._view_option,
            OptionObject,
            offer_id=offer_id,
            id=id,
            locale=locale,
        )

    async def create_many(
            self,
            offer_id: int,
            body: OptionListType | OptionParametr,
            locale: Locale | str = "ru",
    ) -> ApiResult:
        """
        See Option.create_many
        """
        return await async_handler_api(
            self.client,
            self._create_many,
            OptionObject,
            offer_id=offer_id,
            body=body,
            locale=locale,
        )

    async def list_active_offer_options(
            self,
            offer_id: int,
            locale: Locale | str = "ru",
    ) -> ApiResult:
        """
        See Option.list_active_offer_options
        """
        return await async_handler_api(
            self.client,
            self._list_active_offer_options,
            OptionObject,
            offer_id=offer_id,
            locale=locale,
        )

    async def archive_options(
            self,
            offer_id: int,
            options_ids: int | list[int, ...],
            locale: Locale | str = "ru",
            delete_all: bool = False,
    ) -> ApiResult:
        """
        See Option.archive_options
        """
        return await async_handler_api(
            self.client,
            self._archive_options,
            SuccessObject,
            offer_id=offer_id,
            locale=locale,
            options_ids=options_ids,
            delete_all=delete_all,
        )

    async def create_or_update_variants(
            self,
            offer_id: int,
            option_id: int,
            body: OptionValue | OptionValueListType,
            locale: Locale | str = "ru",
    ) -> ApiResult:
        """
        See Option.create_or_update_variants
        """
        return await async_handler_api(
            self.client,
            self._create_or_update_variants,
            OptionValueObject,
            offer_id=offer_id,
            locale=locale,
            option_id=option_id,
            body=body,
        )

    async def archive_option_variants_asynchronously(
            self,
            offer_id: int,
            option_id: int,
            option_variant_ids: list[int] | int,
            locale: Locale | str = "ru",
            delete_all: bool = False,
    ):
        """
        See Option.archive_option_variants_asynchronously
        """
        return await async_handler_api(
            self.client,
            self._archive_option_variants_asynchronously,
            SuccessObject,
            offer_id=offer_id,
            locale=locale,
            option_id=option_id,
            option_variant_ids=option_variant_ids,
            delete_all=delete_all,
        )
