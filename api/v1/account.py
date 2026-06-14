from api.v1.category import Category
from schemas.balance_object import BalanceObject


class Account(Category):
    def seller_balance_info(self) -> BalanceObject:
        response = self.client.get("sellers/account/balance/info")
        data = response.json()

        return BalanceObject(**data)
