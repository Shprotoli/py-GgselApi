from json import dumps

from api.category import Category, RouteApiV1


class ApiLoginBaseV1(Category, RouteApiV1):
    def _api_login(self, seller_id: int, timestamp: int, sign: str) -> dict[str, str]:
        """
        This method converts the input arguments into arguments for `request` and `httpx`
        """
        payload = {
            "seller_id": seller_id,
            "timestamp": str(timestamp),
            "sign": sign,
        }

        return {
            "route": "apilogin",
            "data": dumps(payload),
        }
