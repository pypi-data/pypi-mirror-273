import json
import re
import warnings
from typing import List, Union

import requests

from zaiclient import config
from zaiclient.auth import ZaiHmacAuth
from zaiclient.exceptions.BatchSizeLimitExceededException import (
    BatchSizeLimitExceededException,
)
from zaiclient.exceptions.EmptyBatchException import EmptyBatchException
from zaiclient.exceptions.InputTypeNotEqualException import InputTypeNotEqualException
from zaiclient.exceptions.ZaiClientException import ZaiClientException
from zaiclient.request.Events.EventRequest import EventRequest
from zaiclient.request.Items.ItemRequest import ItemRequest
from zaiclient.request.Recommendations.RecommendationRequest import (
    RecommendationRequest,
)
from zaiclient.request.Request import Request
from zaiclient.response.EventLoggerResponse import EventLoggerResponse
from zaiclient.response.ItemResponse import ItemResponse
from zaiclient.response.RecommendationResponse import RecommendationResponse


class ZaiClient(object):
    def __init__(
        self,
        client_id: str,
        secret: str,
        connect_timeout: Union[int, float] = config.CONNECT_TIMEOUT_S,
        read_timeout: Union[int, float] = config.READ_TIMEOUT_S,
        custom_endpoint: str = "",
    ):
        if isinstance(client_id, str) is False:
            raise TypeError("Client ID must be a string value.")
        if isinstance(secret, str) is False:
            raise TypeError("Secret must be a string value.")
        if isinstance(connect_timeout, (int, float)) is False:
            raise TypeError("Connect Timeout must be an integer or a float value.")
        if isinstance(read_timeout, (int, float)) is False:
            raise TypeError("Read Timeout must be an integer or a float value.")
        if isinstance(custom_endpoint, str) is False:
            raise TypeError("Custom Endpoint must be a string value.")
        if len(custom_endpoint) > 100:
            raise ValueError("Custom Endpoint must be less than or equal to 100.")
        if re.match("^[a-zA-Z0-9-]*$", custom_endpoint) is None:
            raise ValueError("Only alphanumeric characters are allowed for custom endpoint.")

        __connect_timeout = connect_timeout
        if connect_timeout <= 0:
            __connect_timeout = config.CONNECT_TIMEOUT_S
        __read_timeout = read_timeout
        if read_timeout <= 0:
            __read_timeout = config.READ_TIMEOUT_S

        self.__custom_endpoint = "" if custom_endpoint == "" else f"-{custom_endpoint}"

        self.__client_id = client_id
        self.__auth = ZaiHmacAuth(client_id, secret)
        self.__timeout = (__connect_timeout, __read_timeout)
        self.__session = requests.Session()

    def __process_base_url(self, base_url: str) -> str:
        return base_url.format(self.__custom_endpoint)

    def __send_request(self, method: str, url: str, payload, headers={}, params={}):
        response = requests.Response()
        try:
            response = self.__session.request(
                method=method,
                url=url,
                params=params,
                data=None,
                json=payload,
                headers=headers,
                cookies=None,
                files=None,
                auth=self.__auth,
                timeout=self.__timeout,
                verify=True,
            )
            response.raise_for_status()
        except requests.HTTPError as http_err:
            raise ZaiClientException(http_err)

        return response.json()

    def send_request(
        self, request: Union[Request, List[Request]], is_test: bool = False
    ) -> Union[EventLoggerResponse, RecommendationResponse, ItemResponse]:
        response = None

        if isinstance(request, EventRequest):
            payload = request.get_payload(is_test=is_test)

            response = self.__send_request(
                method=request.method.value,
                url=self.__process_base_url(request.base_url) + request.get_path(self.__client_id),
                payload=payload,
                params=request.get_query_param(),
            )

            return EventLoggerResponse(**response)

        elif isinstance(request, RecommendationRequest):
            payload = request.get_payload(is_test=is_test).dict()

            response = self.__send_request(
                method=request.method.value,
                url=self.__process_base_url(request.base_url) + request.get_path(self.__client_id),
                payload=payload,
                params=request.get_query_param(),
            )

            try:
                response["metadata"] = json.loads(response["metadata"])
            except Exception as error:
                warnings.warn(
                    f"Failed to parse the metadata to object, returning an empty object. Error Message: {error}"
                )
                response["metadata"] = {}

            return RecommendationResponse(**response)

        elif isinstance(request, ItemRequest):
            payload = request.get_payload(is_test=is_test)

            response = self.__send_request(
                method=request.method.value,
                url=self.__process_base_url(request.base_url) + request.get_path(self.__client_id),
                payload=payload,
                params=request.get_query_param(),
            )

            return ItemResponse(**response)

        elif isinstance(request, list):
            if len(request) == 0:
                raise EmptyBatchException()

            if not isinstance(request[0], Request):
                raise TypeError()

            if not all(isinstance(item_request, type(request[0])) for item_request in request):
                raise InputTypeNotEqualException()

            if len(request) > config.BATCH_REQUEST_CAP:
                raise BatchSizeLimitExceededException()

            item_payload = [item.get_payload(is_test=is_test) for item in request]
            _query_params = [item.get_query_param() for item in request]

            query_params = {}
            for key in _query_params[0].keys():
                query_params[key] = []

            for query_param in _query_params:
                for key in query_param:
                    if key in query_params:
                        query_params[key].append(query_param[key])

            response = self.__send_request(
                method=request[0].method.value,
                url=self.__process_base_url(request[0].base_url) + request[0].get_path(self.__client_id),
                payload=item_payload,
                params=query_params,
            )

            return ItemResponse(**response)

        else:
            raise TypeError()
