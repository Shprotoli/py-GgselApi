# Requests of the `ApiLogin` category of the GGSel API
from ggsel_py.api.category import Category, AsyncCategory, RouteApiV1, RequestSpec, build_request, endpoint
from ggsel_py.parameters.api import EnumCrudMethod
from ggsel_py.schemas.v1.token_object import TokenObject


class ApiLoginEndpointsV1(Category, RouteApiV1):
    @endpoint(TokenObject)
    def api_login(self, seller_id: int, timestamp: int | str, sign: str) -> RequestSpec:
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
        api_login_category = api_obj.api_login
        TOKEN = api_login_category.api_login(ID_SELLER, int(timestamp), sign).token

        api_obj.set_token(TOKEN)
        ```

        :param seller_id: Your seller ID, which can be viewed in your GGSel profile
        :param timestamp: Unix Time Stamp
        :param sign: Your SHA256(API-key + timestamp)
        """
        payload = {
            "seller_id": seller_id,
            "timestamp": str(timestamp),
            "sign": sign,
        }

        return build_request(EnumCrudMethod.POST, "apilogin", payload=payload)


class ApiLogin(ApiLoginEndpointsV1):
    pass


class AsyncApiLogin(AsyncCategory, ApiLoginEndpointsV1):
    pass
