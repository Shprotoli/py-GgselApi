# A class file that handles requests from the `Account` category of the GGSell API
from datetime import datetime

from tools.formated import format_dt
from api.v1.category import Category
from schemas.balance_object import BalanceObject
from schemas.receipts_object import ReceiptsObject


class Account(Category):
    def seller_balance_info(self) -> BalanceObject:
        """
        Source docs: https://seller.ggsel.com/docs/return-seller-balance-info
        This function makes a request to retrieve the user's balance.

        :return: dataclass BalanceObject containing a json response from the API
        """
        response = self.client.get("sellers/account/balance/info")
        data = response.json()

        return BalanceObject(**data)

    def seller_receipts(
            self,
            page: str,
            count: int,
            currency: str = "",
            type: str = "",
            code_filter: str = "",
            allow_type: str = "",
            start: str | datetime = "",
            finish: str | datetime = "",
    ) -> ReceiptsObject:
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
        response = self.client.get("sellers/account/receipts", params=params)
        data = response.json()

        return ReceiptsObject(**data)
