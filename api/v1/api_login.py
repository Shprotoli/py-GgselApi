from json import dumps

from api.client import GClient
from schemas.token_object import TokenObject
from api.v1.category import Category


class ApiLogin(Category):
    def api_login(self, seller_id: int, timestamp: str | int, sign: str) -> TokenObject:
        payload = dumps({
            "seller_id": seller_id,
            "timestamp": str(timestamp),
            "sign": sign,
        })

        response = self.client.post("apilogin", data=payload)
        data = response.json()
        return TokenObject(**data)
