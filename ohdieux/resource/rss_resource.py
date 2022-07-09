from datetime import datetime
import os

from jinja2 import Template
from jivago.lang.annotations import Inject
from jivago.lang.stream import Stream
from jivago.wsgi.annotations import Resource
from jivago.wsgi.invocation.parameters import QueryParam
from jivago.wsgi.methods import GET
from jivago.templating.rendered_view import RenderedView

from ohdieux.model.episode_descriptor import EpisodeDescriptor, MediaDescriptor
from ohdieux.ohdio.ohdio_reader import OhdioReader


@Resource("/rss")
class RssResource(object):

    @Inject
    def __init__(self, ohdio_reader: OhdioReader):
        self._ohdio_reader = ohdio_reader

    @GET
    def get_manifest(self, programme_id: QueryParam[str]):
        programme = self._ohdio_reader.query(str(programme_id))
        return RenderedView("manifest.xml",
                            {"programme": programme.programme,
                             "episodes": Stream(programme.episodes)
                            .map(lambda x: EpisodeDescriptor(x.title, x.description, x.guid, x.date, x.duration,
                                                             MediaDescriptor(x.media.media_url, x.media.media_type,
                                                                             x.media.length))
                                 ).toList(),
                             "now": datetime.now().isoformat()
                             }, content_type="text/xml")
