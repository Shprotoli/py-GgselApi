from requests import Response
import requests


class GClient:
    def __init__(
            self,
            protocol: str = "https",
            domain: str = "seller.ggsel.com",
            base_route: str = "api_sellers/api",
    ):
        self.protocol = protocol.lower()
        self.domain = domain

        self._base_route = base_route

        self.headers = {"Content-Type": "application/json"}
        self.params: dict = {}

    def set_token(self, token: str) -> None:
        self.params['token'] = token

    @property
    def base_url(self) -> str:
        return f"{self.protocol}://{self.domain}/{self._base_route}"

    def request(self, route: str, method: str, **kwargs) -> Response:
        request_url = f"{self.base_url}/{route}"
        response = requests.request(method, request_url, **kwargs)

        return response

    def get(self, route: str, **kwargs) -> Response:
        return self.request(route, "get", headers=self.headers, params=self.params, **kwargs)

    def post(self, route: str, **kwargs) -> Response:
        return self.request(route, "post", headers=self.headers, params=self.params, **kwargs)

    def put(self, route: str, **kwargs) -> Response:
        return self.request(route, "put", headers=self.headers, params=self.params, **kwargs)
