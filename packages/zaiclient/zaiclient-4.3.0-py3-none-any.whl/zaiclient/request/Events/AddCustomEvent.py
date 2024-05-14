import time
from typing import List, Union

from zaiclient.exceptions.InputLengthNotEqualException import (
    InputLengthNotEqualException,
)
from zaiclient.exceptions.InputTypeNotEqualException import InputTypeNotEqualException
from zaiclient.request.Events.EventRequest import EventRequest


class AddCustomEvent(EventRequest):
    def __init__(
        self,
        user_id: str,
        item_ids: Union[str, List[str]],
        event_type: str,
        event_values: Union[str, List[str]],
        timestamp: Union[float, None] = None,
        from_: Union[str, List[str], None] = None,
        is_zai_rec: Union[bool, List[bool], None] = None,
        url: Union[str, None] = None,
        ref: Union[str, None] = None,
        user_properties: dict = {},
        event_properties: dict = {},
    ):
        if from_ is None:
            _from = "" if isinstance(item_ids, str) else [""] * len(item_ids)
        else:
            _from = from_

        if is_zai_rec is None:
            _is_zai_rec = False if isinstance(item_ids, str) else [False] * len(item_ids)
        else:
            _is_zai_rec = is_zai_rec

        if not isinstance(user_id, str):
            raise TypeError("User ID must be a string value.")

        if not isinstance(event_type, str):
            raise TypeError("Event Type must be a string value.")

        if (
            type(item_ids) != type(event_values)
            or type(item_ids) != type(_from)
            or isinstance(item_ids, List) != isinstance(_is_zai_rec, List)
        ):
            raise InputTypeNotEqualException()

        if (
            isinstance(item_ids, List)
            and isinstance(event_values, List)
            and isinstance(_from, List)
            and isinstance(_is_zai_rec, List)
            and not (
                all(isinstance(item_id, str) for item_id in item_ids)
                and all(isinstance(event_value, str) for event_value in event_values)
                and all(isinstance(_from_, str) for _from_ in _from)
                and all(isinstance(_is_zai_rec_, bool) for _is_zai_rec_ in _is_zai_rec)
            )
        ):
            raise InputTypeNotEqualException()

        if url is not None and not isinstance(url, str):
            raise TypeError("Url must be a string value.")

        if ref is not None and not isinstance(ref, str):
            raise TypeError("Ref must be a string value.")

        _item_ids = [item_ids] if isinstance(item_ids, str) else item_ids
        _event_values = [event_values] if isinstance(event_values, str) else event_values
        _timestamp = timestamp if timestamp is not None else time.time()
        from_values = [_from] if isinstance(_from, str) else _from
        is_zai_recommendations = [_is_zai_rec] if isinstance(_is_zai_rec, bool) else _is_zai_rec

        if (
            len(_item_ids) != len(_event_values)
            or len(_item_ids) != len(from_values)
            or len(_item_ids) != len(is_zai_recommendations)
        ):
            raise InputLengthNotEqualException()

        super().__init__(
            user_id,
            _item_ids,
            _timestamp,
            event_type,
            _event_values,
            from_values,
            is_zai_recommendations,
            url,
            ref,
            user_properties,
            event_properties,
        )
