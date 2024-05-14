import time
from typing import Union

from zaiclient.request.Events.EventRequest import EventRequest


class AddCartaddEvent(EventRequest):
    __default_event_type = "cartadd"
    __default_event_value = "null"

    def __init__(
        self,
        user_id: str,
        item_id: str,
        timestamp: Union[float, None] = None,
        from_: Union[str, None] = None,
        is_zai_rec: bool = False,
        url: Union[str, None] = None,
        ref: Union[str, None] = None,
        user_properties: dict = {},
        event_properties: dict = {},
    ):
        if not isinstance(user_id, str):
            raise TypeError("User ID must be a string value.")

        if not isinstance(item_id, str):
            raise TypeError("Item ID must be a string value.")

        if from_ is not None and not isinstance(from_, str):
            raise TypeError("From must be a string value.")

        if not isinstance(is_zai_rec, bool):
            raise TypeError("is_zai_rec must be a boolean value.")

        if url is not None and not isinstance(url, str):
            raise TypeError("Url must be a string value.")

        if ref is not None and not isinstance(ref, str):
            raise TypeError("Ref must be a string value.")

        _item_ids = [item_id]
        _event_values = [self.__default_event_value]
        _timestamp = timestamp if timestamp is not None else time.time()
        from_values = [from_]
        is_zai_recommendations = [is_zai_rec]

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
