from pydantic import BaseModel, confloat, conint, conlist

from zaiclient.request.Items.Item import Item


class ItemResponse(BaseModel):
    items: conlist(item_type=Item)
    count: conint(ge=0)
    timestamp: confloat(ge=1_648_871_097.0, le=2_147_483_647.0)
