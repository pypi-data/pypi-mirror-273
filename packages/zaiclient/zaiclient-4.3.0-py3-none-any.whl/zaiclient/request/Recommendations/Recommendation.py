from typing import Union

from pydantic import BaseModel, conint, conlist, constr


class Recommendation(BaseModel):
    user_id: Union[constr(min_length=1, max_length=500), None] = None
    item_id: Union[constr(min_length=1, max_length=500), None] = None
    item_ids: Union[conlist(item_type=constr(min_length=1, max_length=500), min_items=0, max_items=10_000), None] = None
    limit: conint(ge=0, le=10_000)
    offset: conint(ge=0, le=10_000) = 0
    options: Union[constr(min_length=0, max_length=1000), None] = None
    recommendation_type: constr(min_length=1, max_length=500)

    class Config:
        schema_extra = {"example": {"user_id": "123456", "limit": 30, "offset": 0, "recommendation_type": "homepage"}}
