from typing import Union

from jivago.wsgi.invocation.parameters import OptionalQueryParam, QueryParam


def parse_bool(
        query_param: Union[str, QueryParam[str],
                           OptionalQueryParam[str]]) -> bool:
    return query_param in ("t", "true", "True", "1", "y", "yes")
