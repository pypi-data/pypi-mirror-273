import time
from typing import List, Union

from zaiclient.exceptions.InputLengthNotEqualException import (
    InputLengthNotEqualException,
)
from zaiclient.exceptions.InputTypeNotEqualException import InputTypeNotEqualException
from zaiclient.request.Events.EventRequest import EventRequest


class AddPurchaseEvent(EventRequest):
    __default_event_type = "purchase"

    def __init__(
        self,
        user_id: str,
        item_ids: Union[str, List[str]],
        prices: Union[int, List[int]],
        timestamp: Union[float, None] = None,
        is_zai_rec: Union[bool, List[bool], None] = None,
        url: Union[str, None] = None,
        ref: Union[str, None] = None,
        user_properties: dict = {},
        event_properties: dict = {},
    ):
        if is_zai_rec is None:
            _is_zai_rec = False if isinstance(item_ids, str) else [False] * len(item_ids)
        else:
            _is_zai_rec = is_zai_rec

        if not isinstance(user_id, str):
            raise TypeError("User ID must be a string value.")

        if not (
            isinstance(item_ids, List) == isinstance(prices, List)
            and isinstance(item_ids, List) == isinstance(_is_zai_rec, List)
        ):
            raise InputTypeNotEqualException()

        if (
            isinstance(item_ids, List)
            and isinstance(prices, List)
            and isinstance(_is_zai_rec, List)
            and not (
                all(isinstance(item_id, str) for item_id in item_ids)
                and all(isinstance(price, int) for price in prices)
                and all(isinstance(is_zai_rec_, bool) for is_zai_rec_ in _is_zai_rec)
            )
        ):
            raise InputTypeNotEqualException()

        _item_ids = [item_ids] if isinstance(item_ids, str) else item_ids
        _event_values = [str(prices)] if isinstance(prices, int) else [str(price) for price in prices]
        _timestamp = timestamp if timestamp is not None else time.time()
        from_values = [None] * len(_item_ids)
        is_zai_recommendations = [_is_zai_rec] if isinstance(_is_zai_rec, bool) else _is_zai_rec

        if len(_item_ids) != len(_event_values) or len(_item_ids) != len(is_zai_recommendations):
            raise InputLengthNotEqualException()

        if url is not None and not isinstance(url, str):
            raise TypeError("Url must be a string value.")

        if ref is not None and not isinstance(ref, str):
            raise TypeError("Ref must be a string value.")

        super().__init__(
            user_id,
            _item_ids,
            _timestamp,
            self.__default_event_type,
            _event_values,
            from_values,
            is_zai_recommendations,
            url,
            ref,
            user_properties,
            event_properties,
        )
