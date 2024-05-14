from pydantic import constr

from zaiclient import http
from zaiclient.request.Items.ItemRequest import ItemRequest


class UpdateItem(ItemRequest):
    def __init__(self, item_id: constr(min_length=1, max_length=500), properties: dict = {}):
        super().__init__(
            http.HTTPMethod.PUT,
            id=item_id,
            name=properties["item_name"] if "item_name" in properties else None,
            properties=properties,
        )
