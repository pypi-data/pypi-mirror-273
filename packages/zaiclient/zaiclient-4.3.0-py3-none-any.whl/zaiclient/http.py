# HTTP Verbs
from enum import Enum

GET = "GET"
POST = "POST"
PUT = "PUT"
PATCH = "PATCH"
HEAD = "HEAD"
DELETE = "DELETE"
OPTIONS = "OPTIONS"


class HTTPMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
