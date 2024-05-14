from datetime import datetime
from typing import Union

from pydantic import BaseModel, confloat, conint, constr


class Item(BaseModel):
    item_id: constr(min_length=1, max_length=500)
    item_name: Union[constr(min_length=1, max_length=2000), None] = None
    category_id_1: Union[constr(min_length=0, max_length=2000), None] = None
    category_name_1: Union[constr(min_length=0, max_length=2000), None] = None
    category_id_2: Union[constr(min_length=0, max_length=2000), None] = None
    category_name_2: Union[constr(min_length=0, max_length=2000), None] = None
    category_id_3: Union[constr(min_length=0, max_length=2000), None] = None
    category_name_3: Union[constr(min_length=0, max_length=2000), None] = None
    brand_id: Union[constr(min_length=0, max_length=2000), None] = None
    brand_name: Union[constr(min_length=0, max_length=2000), None] = None
    description: Union[constr(min_length=0, max_length=65535), None] = None
    created_timestamp: Union[datetime, None] = None
    updated_timestamp: Union[datetime, None] = None
    is_active: Union[bool, None] = None
    is_soldout: Union[bool, None] = None
    promote_on: Union[constr(min_length=0, max_length=2000), None] = None
    item_group: Union[constr(min_length=0, max_length=2000), None] = None
    rating: Union[confloat(ge=0.0), None] = None
    price: Union[confloat(ge=0.0), None] = None
    click_counts: Union[conint(ge=0), None] = None
    purchase_counts: Union[conint(ge=0), None] = None
    image_url: Union[constr(min_length=0, max_length=2000), None] = None
    item_url: Union[constr(min_length=0, max_length=2000), None] = None
    miscellaneous: Union[constr(min_length=0, max_length=65535), None] = None
