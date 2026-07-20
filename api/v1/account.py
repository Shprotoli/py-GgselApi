# A class file that handles requests from the `Account` category of the GGSell API
from datetime import datetime

from tools.handlers import handler_api, async_handler_api, EnumMethodHandle, ApiResult
from parameters.account import Type, CodeFilter
from schemas.v1.balance_object import BalanceObject
from schemas.v1.receipts_object import ReceiptsObject
from api.base.account import AccountBaseV1


class Account(AccountBaseV1):
    def seller_balance_info(self) -> ApiResult:
        """
        Source docs: https://seller.ggsel.com/docs/return-seller-balance-info
        This function makes a request to retrieve the user's balance.

        :return: dataclass BalanceObject containing a json response from the API
        """
        return handler_api(
            EnumMethodHandle.GET,
            self.client,
            self._seller_balance_info,
            BalanceObject
        )

    def seller_receipts(
            self,
            page: int = 1,
            count: int = 100,
            currency: str = "",
            type: str | Type = "",
            code_filter: str | CodeFilter = "",
            allow_type: str | Type = "",
            start: str | datetime = "",
            finish: str | datetime = "",
    ) -> ApiResult:
        """
        Source docs: https://seller.ggsel.com/docs/return-seller-receipts
        This function retrieves a list of financial transactions from the page `https://seller.ggsel.com/finance`
        using the specified parameters and filters.

        :param page: Page number (compare with the page number from `https://seller.ggsel.com/finance`)
        :param count: Number of operations (from more relevant to less relevant)
        :param currency: Currency type
        :param type: Filter for the type of operation to be performed (You cannot select multiple options)
        :param code_filter: [OBSOLETE] Filter whether the Digiseller unique order code is verified or not
        :param allow_type: [NOT WORKING] Enumeration of operation type filter, similar to the `type` parameter,
                           but accepts multiple types
        :param start: {Format date/time: ISO 8601} Operations not earlier than a specified date
        :param finish: {Format date/time: ISO 8601} Operations no later than the specified set date
        :return: dataclass ReceiptsObject containing a json response from the API
        """
        return handler_api(
            EnumMethodHandle.GET,
            self.client,
            self._seller_receipts,
            ReceiptsObject,
            page=page,
            count=count,
            currency=currency,
            type=type,
            code_filter=code_filter,
            allow_type=allow_type,
            start=start,
            finish=finish
        )


class AsyncAccount(AccountBaseV1):
    async def seller_balance_info(self) -> ApiResult:
        """
        See Account.seller_balance_info
        """
        return await async_handler_api(
            EnumMethodHandle.GET,
            self.client,
            self._seller_balance_info,
            BalanceObject
        )

    async def seller_receipts(
            self,
            page: int = 1,
            count: int = 100,
            currency: str = "",
            type: str | Type = "",
            code_filter: str | CodeFilter = "",
            allow_type: str | Type = "",
            start: str | datetime = "",
            finish: str | datetime = "",
    ) -> ApiResult:
        """
        See Account.seller_receipts
        """
        return await async_handler_api(
            EnumMethodHandle.GET,
            self.client,
            self._seller_receipts,
            ReceiptsObject,
            page=page,
            count=count,
            currency=currency,
            type=type,
            code_filter=code_filter,
            allow_type=allow_type,
            start=start,
            finish=finish
        )
