# A class file that handles requests from the `ApiLogin` category of the GGSell API
from abc import abstractmethod
from json import dumps
from typing import Union

from tools.handlers import handler_response_api, ApiResult
from schemas.token_object import TokenObject
from api.v1.category import Category


class ApiLoginBase(Category):
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


class ApiLogin(ApiLoginBase):
    def api_login(self, seller_id, timestamp, sign) -> ApiResult:
        """
        Source docs: https://seller.ggsel.com/docs/return-seller-token
        This function allows you to generate a token using the API key that was obtained on the page `https://seller.ggsel.com/settings`.

        The token obtained using this method is required for each handle in the GGSel API and is passed as a parameter
        in the request. Once obtained, you can set it in the `GClient` using the `set_token` method.

        Here is the official instruction for obtaining a token using this method:

        1) Follow the link https://emn178.github.io/online-tools/sha256.html
        2) Use the API key that was sent to your email (API Settings section).
        3) In the devtools console, enter the command: Date.now() = and combine your API key and timestamp value.
        4) The Output field will display the result, which is the value of the sign parameter.
        5) Paste the result from step 3 into the timestamp

        This part can be tricky, so here's a piece of code to get the token:
        ```python
        from time import time
        from hashlib import sha256

        from ggsel_py.api.ggsel_api import GgselApiV1


        ID_SELLER = 111111111
        API_KEY = "..."

        timestamp = str(int(time() * 1000))
        sign = sha256((API_KEY + timestamp).encode()).hexdigest()

        api_obj = GgselApiV1()
        api_login_category = api_obj.ApiLogin
        TOKEN = api_login_category.api_login(ID_SELLER, int(timestamp), sign).token

        api_obj.set_token(TOKEN)
        ```

        :param seller_id: Your seller ID, which can be viewed in your GGSel profile
        :param timestamp: Unix Time Stamp
        :param sign: Your SHA256(API-key + timestamp), this like:
                ```python
                from time import time
                from hashlib import sha256

                API_KEY = "..."

                timestamp = str(int(time() * 1000))
                sign = sha256((API_KEY + timestamp).encode()).hexdigest()
                ```
        :return: dataclass TokenObject containing a json response from the API
        """
        response = self.client.post(**self._api_login(seller_id, timestamp, sign))
        return handler_response_api(TokenObject, response.json())


class AsyncApiLogin(ApiLoginBase):
    async def api_login(self, seller_id: int, timestamp: Union[str | int], sign: str) -> ApiResult:
        """
        See ApiLoginBase.api_login
        """
        response = await self.client.post(**self._api_login(seller_id, timestamp, sign))
        return handler_response_api(TokenObject, response.json())
