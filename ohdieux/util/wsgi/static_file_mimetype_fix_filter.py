from jivago.inject.annotation import Component
from jivago.lang.annotations import Override
from jivago.wsgi.filter.filter import Filter
from jivago.wsgi.filter.filter_chain import FilterChain
from jivago.wsgi.request.request import Request
from jivago.wsgi.request.response import Response


@Component
class StaticFileMimetypeFixFilter(Filter):

    @Override
    def doFilter(self, request: Request, response: Response,
                 chain: FilterChain):
        chain.doFilter(request, response)
        if request.path.endswith(".js"):
            response.headers["Content-Type"] = "text/javascript"
        if request.path.endswith(".png"):
            response.headers["Content-Type"] = "image/png"
