from api.client import GClient
from api.v1.api_login import ApiLogin
from api.v1.account import Account


class GgselApiV1:
    __slots__ = ["client", "ApiLogin", "Account"]

    def __init__(self, token: str = "", client: GClient | None = None):
        self.client = client or GClient()
        self.client.set_token(token)

        self.ApiLogin = ApiLogin(self.client)
        self.Account = Account(self.client)