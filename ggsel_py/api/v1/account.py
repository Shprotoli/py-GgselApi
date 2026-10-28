# Requests of the `Account` category of the GGSel API
from datetime import datetime

from ggsel_py.api.category import Category, AsyncCategory, RouteApiV1, RequestSpec, build_request, endpoint
from ggsel_py.parameters.account import Type, CodeFilter
from ggsel_py.parameters.api import EnumCrudMethod
from ggsel_py.schemas.v1.balance_object import BalanceObject
from ggsel_py.schemas.v1.receipts_object import ReceiptsObject
from ggsel_py.tools.formated import format_dt


class AccountEndpointsV1(Category, RouteApiV1):
    @endpoint(BalanceObject)
    def seller_balance_info(self) -> RequestSpec:
        """
        Source docs: https://seller.ggsel.com/docs/return-seller-balance-info
        """
        return build_request(EnumCrudMethod.GET, "sellers/account/balance/info")

    @endpoint(ReceiptsObject)
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
    ) -> RequestSpec:
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
        """
        params = {
            "page": page,
            "count": count,
            "currency": currency,
            "type": type,
            "code_filter": code_filter,
            "allow_type": allow_type,
            "start": format_dt(start),
            "finish": format_dt(finish),
        }

        return build_request(EnumCrudMethod.GET, "sellers/account/receipts", params=params)


class Account(AccountEndpointsV1):
    pass


class AsyncAccount(AsyncCategory, AccountEndpointsV1):
    pass
