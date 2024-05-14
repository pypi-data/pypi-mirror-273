import json
import re
from typing import List, Union

from zaiclient import config
from zaiclient.request.Recommendations.RecommendationRequest import (
    RecommendationRequest,
)


class GetCustomRecommendation(RecommendationRequest):
    __default_offset = 0

    def __init__(
        self,
        recommendation_type: str,
        limit: int,
        offset: int = __default_offset,
        user_id: Union[str, None] = None,
        item_id: Union[str, None] = None,
        item_ids: Union[List[str], None] = None,
        options: Union[dict, None] = None,
    ):
        if self._validate_recommendation_type(recommendation_type) is None:
            raise ValueError("Recommendation Type must be in the format of ^[0-9a-zA-Z-_]+$")

        if user_id is None and item_id is None and item_ids is None:
            raise ValueError("At least one of userId, itemId, or itemIds must be provided.")

        _options = options

        if options is not None:
            _options = json.dumps(options)

        super().__init__(
            user_id=user_id,
            item_id=item_id,
            item_ids=item_ids,
            limit=limit,
            offset=offset,
            recommendation_type=recommendation_type,
            options=_options,
        )

    def get_path(self, client_id: str) -> str:
        return config.ML_API_PATH_PREFIX.format(client_id) + config.CUSTOM_RECOMMENDATION_PATH_PREFIX

    def _validate_recommendation_type(self, recommendation_type: str):
        pattern = re.compile("^[a-zA-Z0-9-_]+$")
        matcher = pattern.match(recommendation_type)

        return matcher
