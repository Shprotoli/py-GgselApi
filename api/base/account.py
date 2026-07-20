from datetime import datetime
from typing import Any, Type

from parameters.account import CodeFilter
from tools.formated import format_dt
from api.category import Category, RouteApiV1


class AccountBaseV1(Category, RouteApiV1):
    def _seller_balance_info(self) -> dict[str, Any]:
        return {
            "route": "sellers/account/balance/info",
        }

    def _seller_receipts(
            self,
            page: int = 1,
            count: int = 100,
            currency: str = "",
            type: str | Type = "",
            code_filter: str | CodeFilter = "",
            allow_type: str | Type = "",
            start: str | datetime = "",
            finish: str | datetime = "",
    ) -> dict[str, Any]:
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
