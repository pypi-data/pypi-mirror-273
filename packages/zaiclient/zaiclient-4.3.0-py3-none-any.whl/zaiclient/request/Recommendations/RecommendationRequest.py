from typing import List, Union

from zaiclient import config, http
from zaiclient.request.Recommendations.Recommendation import Recommendation
from zaiclient.request.Request import Request


class RecommendationRequest(Request):
    def __init__(
        self,
        user_id: Union[str, None],
        item_id: Union[str, None],
        item_ids: Union[List[str], None],
        recommendation_type: str,
        limit: int,
        offset: int = 0,
        options: Union[str, None] = None,
    ):
        super().__init__(http.HTTPMethod.POST, config.ML_API_ENDPOINT)

        self._payload = Recommendation(
            user_id=user_id,
            item_id=item_id,
            item_ids=item_ids,
            recommendation_type=recommendation_type,
            limit=limit,
            offset=offset,
            options=options,
        )

    def get_path(self, client_id: str) -> str:
        return ""

    def get_payload(self, is_test: bool = False):
        return self._payload

    def get_query_param(self):
        return {}
