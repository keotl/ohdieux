from jivago.templating.rendered_view import RenderedView
from jivago.wsgi.annotations import Resource, Path
from jivago.wsgi.methods import GET


@Resource("/")
class IndexResource(object):

    @GET
    def get(self):
        return RenderedView("index.html", {})

