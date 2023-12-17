from jivago.templating.rendered_view import RenderedView
from jivago.wsgi.annotations import Resource
from jivago.wsgi.methods import GET
from jivago.wsgi.request.response import Response


@Resource("/")
class IndexResource(object):

    @GET
    def get(self):
        return Response(
            200, {
                "Cache-Control":
                "max-age=1800, stale-while-revalidate=60, stale-if-error=86400"
            }, RenderedView("index.html", {}))
