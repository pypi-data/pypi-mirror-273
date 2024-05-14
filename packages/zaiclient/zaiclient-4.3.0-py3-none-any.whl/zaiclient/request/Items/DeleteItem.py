from pydantic import constr

from zaiclient import http
from zaiclient.request.Items.ItemRequest import ItemRequest


class DeleteItem(ItemRequest):
    def __init__(
        self,
        item_id: constr(min_length=1, max_length=500),
    ):
        super().__init__(http.HTTPMethod.DELETE, item_id)

        self.item_id = item_id

    def get_query_param(self):
        return {"id": self.item_id}
