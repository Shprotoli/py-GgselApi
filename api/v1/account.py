# A class file that handles requests from the `Account` category of the GGSell API
from datetime import datetime
from typing import Union

from tools.handlers import handler_response_api, ApiResult
from tools.formated import format_dt
from parameters.account import Type, CodeFilter
from api.v1.category import Category
from schemas.balance_object import BalanceObject
from schemas.receipts_object import ReceiptsObject


class AccountBase(Category):
    def _seller_balance_info(self) -> dict:
        return {
            "route": "sellers/account/balance/info",
        }

    def _seller_receipts(
            self,
            page: int = 1,
            count: int = 100,
            currency: str = "",
            type: Union[str | Type] = "",
            code_filter: Union[str | CodeFilter] = "",
            allow_type: Union[str | Type] = "",
            start: Union[str | datetime] = "",
            finish: Union[str | datetime] = "",
    ) -> dict:
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

        return {
            "route": "sellers/account/receipts",
            "params": params,
        }


class Account(AccountBase):
    def seller_balance_info(self) -> ApiResult:
        """
        Source docs: https://seller.ggsel.com/docs/return-seller-balance-info
        This function makes a request to retrieve the user's balance.

        :return: dataclass BalanceObject containing a json response from the API
        """
        response = self.client.get(**self._seller_balance_info())
        data = response.json()

        return handler_response_api(BalanceObject, data=data)

    def seller_receipts(
            self,
            page: int = 1,
            count: int = 100,
            currency: str = "",
            type: Union[str | Type] = "",
            code_filter: Union[str | CodeFilter] = "",
            allow_type: Union[str | Type] = "",
            start: Union[str | datetime] = "",
            finish: Union[str | datetime] = "",
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
        response = self.client.get(
            **self._seller_receipts(
                page,
                count,
                currency,
                type,
                code_filter,
                allow_type,
                start,
                finish
            ))
        data = response.json()

        return handler_response_api(ReceiptsObject, data=data)


class AsyncAccount(AccountBase):
    async def seller_balance_info(self) -> ApiResult:
        """
        See Account.seller_balance_info
        """
        response = await self.client.get(**self._seller_balance_info())
        data = response.json()

        return handler_response_api(BalanceObject, data=data)

    async def seller_receipts(
            self,
            page: int = 1,
            count: int = 100,
            currency: str = "",
            type: Union[str | Type] = "",
            code_filter: Union[str | CodeFilter] = "",
            allow_type: Union[str | Type] = "",
            start: Union[str | datetime] = "",
            finish: Union[str | datetime] = "",
    ) -> ApiResult:
        """
        See Account.seller_receipts
        """
        response = await self.client.get(
            **self._seller_receipts(
                page,
                count,
                currency,
                type,
                code_filter,
                allow_type,
                start,
                finish
            ))
        data = response.json()

        return handler_response_api(ReceiptsObject, data=data)
