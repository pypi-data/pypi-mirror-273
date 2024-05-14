import json
from typing import Union

from zaiclient import config
from zaiclient.request.Recommendations.RecommendationRequest import (
    RecommendationRequest,
)


class GetUserRecommendation(RecommendationRequest):
    __default_offset = 0
    __default_recommendation_type = "homepage"

    def __init__(
        self,
        user_id: Union[str, None],
        limit: int,
        offset: int = __default_offset,
        recommendation_type: str = __default_recommendation_type,
        options: Union[dict, None] = None,
    ):
        _options = options

        if options is not None:
            _options = json.dumps(options)

        super().__init__(
            user_id=user_id,
            item_id=None,
            item_ids=None,
            limit=limit,
            offset=offset,
            recommendation_type=recommendation_type,
            options=_options,
        )

    def get_path(self, client_id: str) -> str:
        return config.ML_API_PATH_PREFIX.format(client_id) + config.USER_RECOMMENDATION_PATH_PREFIX
