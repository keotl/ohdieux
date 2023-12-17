from jivago.inject.annotation import Component
from jivago.wsgi.filter.filter import Filter
from jivago.wsgi.filter.filter_chain import FilterChain
from jivago.wsgi.request.request import Request
from jivago.wsgi.request.response import Response


@Component
class StaticCacheHeadersFilter(Filter):

    def doFilter(self, request: Request, response: Response,
                 chain: FilterChain):
        chain.doFilter(request, response)
        if "Cache-Control" not in response.headers:
            response.headers[
                "Cache-Control"] = "max-age=1800, stale-while-revalidate=60, stale-if-error=86400"
