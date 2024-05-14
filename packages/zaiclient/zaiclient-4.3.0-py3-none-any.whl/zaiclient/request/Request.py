from zaiclient.http import HTTPMethod


class Request(object):
    def __init__(
        self,
        method: HTTPMethod,
        base_url: str,
    ):
        self.method = method
        self.base_url = base_url

    def get_path(self, client_id: str):
        raise NotImplementedError()

    def get_payload(self, is_test: bool):
        raise NotImplementedError()

    def get_query_param(self):
        raise NotImplementedError()
