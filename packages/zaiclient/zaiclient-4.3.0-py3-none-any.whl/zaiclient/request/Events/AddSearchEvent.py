import time
from typing import Union

from zaiclient.request.Events.EventRequest import EventRequest


class AddSearchEvent(EventRequest):
    __default_event_type = "search"
    __default_item_id = "null"

    def __init__(
        self,
        user_id: str,
        search_query: str,
        timestamp: Union[float, None] = None,
        is_zai_rec: bool = False,
        url: Union[str, None] = None,
        ref: Union[str, None] = None,
        user_properties: dict = {},
        event_properties: dict = {},
    ):
        if not isinstance(user_id, str):
            raise TypeError("User ID must be a string value.")

        if not isinstance(search_query, str):
            raise TypeError("Search Query must be a string value.")

        if not isinstance(is_zai_rec, bool):
            raise TypeError("is_zai_rec must be a boolean value.")

        if url is not None and not isinstance(url, str):
            raise TypeError("Url must be a string value.")

        if ref is not None and not isinstance(ref, str):
            raise TypeError("Ref must be a string value.")

        _item_ids = [self.__default_item_id]
        _event_values = [search_query]
        _timestamp = timestamp if timestamp is not None else time.time()
        is_zai_recommendations = [is_zai_rec]

        super().__init__(
            user_id,
            _item_ids,
            _timestamp,
            self.__default_event_type,
            _event_values,
            [None],
            is_zai_recommendations,
            url,
            ref,
            user_properties,
            event_properties,
        )
