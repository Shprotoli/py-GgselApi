from api.client import GClient


class Category:
    def __init__(self, client: GClient):
        self.client = client