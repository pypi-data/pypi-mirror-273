from . import BaseClient

class SearchClient(BaseClient):
    def __init__(self, api_key: str):
        super().__init__(api_key)