import json
from typing import Union

from zaiclient import config, http
from zaiclient.request.Items.Item import Item
from zaiclient.request.Request import Request


class ItemRequest(Request):
    def __init__(self, method: http.HTTPMethod, id: str, name: Union[str, None] = None, properties: dict = None):
        super().__init__(method=method, base_url=config.COLLECTOR_API_ENDPOINT)

        if properties is None:
            properties = {}

        properties["item_id"] = id
        properties["item_name"] = name

        self._payload = json.loads(Item(**properties).json(exclude_none=True))

    def get_payload(self, is_test: bool = False):
        return self._payload

    def get_path(self, client_id: str):
        return config.ITEMS_API_PATH

    def get_query_param(self):
        return {}
