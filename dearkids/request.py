from roll import Request


class CustomRequest(Request):
    __slots__ = (
        "app",
        "url",
        "path",
        "query_string",
        "_query",
        "method",
        "body",
        "headers",
        "route",
        "_cookies",
        "_form",
        "_files",
        "language",  # Added.
    )
