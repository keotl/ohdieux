import logging
import threading
from datetime import datetime
from email.utils import formatdate

from jivago.lang.annotations import Inject
from jivago.lang.stream import Stream
from jivago.templating.rendered_view import RenderedView
from jivago.wsgi.annotations import Resource
from jivago.wsgi.invocation.parameters import QueryParam
from jivago.wsgi.methods import GET, HEAD

from ohdieux.model.episode_descriptor import EpisodeDescriptor, MediaDescriptor
from ohdieux.service.manifest_service import ManifestService


@Resource("/rss")
class RssResource(object):

    @Inject
    def __init__(self, manifest_service: ManifestService):
        self._manifest_service = manifest_service
        self._logger = logging.getLogger(self.__class__.__name__)

    @GET
    def get_manifest(self, programme_id: QueryParam[str], reverse: bool):
        programme = self._manifest_service.generate_podcast_manifest(str(programme_id), bool(reverse))
        return RenderedView("manifest.xml",
                            {"programme": programme.programme,
                             "episodes": Stream(programme.episodes)
                            .map(lambda x: EpisodeDescriptor(x.title, x.description, x.guid,
                                                             formatdate(float(x.date.strftime("%s"))), x.duration,
                                                             MediaDescriptor(x.media.media_url, x.media.media_type,
                                                                             x.media.length))
                                 ).toList(),
                             "now": formatdate(float(datetime.now().strftime("%s")))
                             }, content_type="text/xml")

    @HEAD
    def headers(self):
        return ""
