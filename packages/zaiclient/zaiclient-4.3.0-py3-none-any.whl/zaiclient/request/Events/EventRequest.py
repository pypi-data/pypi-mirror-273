import json
from typing import List, Union

from zaiclient import config, http
from zaiclient.exceptions.BatchSizeLimitExceededException import (
    BatchSizeLimitExceededException,
)
from zaiclient.exceptions.EmptyBatchException import EmptyBatchException
from zaiclient.request.Events.Event import Event
from zaiclient.request.Request import Request


class EventRequest(Request):
    def __init__(
        self,
        user_id: str,
        item_ids: List[str],
        timestamp: float,
        event_type: str,
        event_values: List[str],
        from_values: List[Union[str, None]],
        is_zai_recommendations: List[bool],
        url: Union[str, None] = None,
        ref: Union[str, None] = None,
        user_properties: dict = {},
        event_properties: dict = {},
    ) -> None:
        events = []
        tmp_timestamp = timestamp
        self._timestamp = timestamp

        super().__init__(http.HTTPMethod.POST, config.COLLECTOR_API_ENDPOINT)

        for item_id, event_value, from_value, is_zai_recommendation in zip(
            item_ids, event_values, from_values, is_zai_recommendations
        ):
            events.append(
                json.loads(
                    Event(
                        user_id=user_id,
                        item_id=item_id,
                        timestamp=tmp_timestamp,
                        event_type=event_type,
                        event_value=event_value[:500],
                        from_=from_value[:500] if from_value is not None and len(from_value) != 0 else None,
                        is_zai_recommendation=is_zai_recommendation,
                        url=url,
                        ref=ref,
                        user_properties=user_properties,
                        event_properties=event_properties,
                    ).json(by_alias=True, exclude_none=True)
                )
            )
            tmp_timestamp += config.EPSILON

        if len(events) > config.BATCH_REQUEST_CAP:
            raise BatchSizeLimitExceededException()

        if len(events) == 0:
            raise EmptyBatchException()

        if len(events) == 1:
            self._payload = events[0]
        else:
            self._payload = events

    def get_timestamp(self):
        return self._timestamp

    def get_path(self, client_id: str) -> str:
        return config.EVENTS_API_PATH

    def get_payload(self, is_test: bool = False):
        if is_test:
            if isinstance(self._payload, list):
                for event in self._payload:
                    event["time_to_live"] = config.TEST_EVENT_TIME_TO_LIVE

            else:
                self._payload["time_to_live"] = config.TEST_EVENT_TIME_TO_LIVE

        return self._payload

    def get_query_param(self):
        return {}
