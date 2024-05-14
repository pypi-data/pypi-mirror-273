from pydantic import constr

from zaiclient import http
from zaiclient.request.Items.ItemRequest import ItemRequest


class AddItem(ItemRequest):
    def __init__(
        self,
        item_id: constr(min_length=1, max_length=500),
        item_name: constr(min_length=1, max_length=2000),
        properties: dict = {},
    ):
        super().__init__(http.HTTPMethod.POST, id=item_id, name=item_name, properties=properties)
