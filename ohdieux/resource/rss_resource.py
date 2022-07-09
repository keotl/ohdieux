import logging
import threading
from datetime import datetime

from jivago.inject.annotation import Singleton
from jivago.lang.annotations import Inject
from jivago.lang.stream import Stream
from jivago.templating.rendered_view import RenderedView
from jivago.wsgi.annotations import Resource
from jivago.wsgi.invocation.parameters import QueryParam
from jivago.wsgi.methods import GET

from ohdieux.config import Config
from ohdieux.model.episode_descriptor import EpisodeDescriptor, MediaDescriptor
from ohdieux.ohdio.ohdio_reader import OhdioReader


@Resource("/rss")
@Singleton
class RssResource(object):

    @Inject
    def __init__(self, ohdio_reader: OhdioReader, config: Config):
        self._ohdio_reader = ohdio_reader
        self._cache = {}
        self._lock = threading.Lock()
        self._cache_refresh_delay = config.cache_refresh_delay_s
        self._logger = logging.getLogger(self.__class__.__name__)

    @GET
    def cached(self, programme_id: QueryParam[str]):
        with self._lock:
            if programme_id not in self._cache:
                self._cache[programme_id] = {"lock": threading.Lock(), "updated": datetime.min, "content": None}

        cache_entry = self._cache[programme_id]
        with cache_entry["lock"]:
            if (datetime.now() - cache_entry["updated"]).total_seconds() > self._cache_refresh_delay:
                self._logger.info(f"Refreshing programme {programme_id}.")
                cache_entry["content"] = self.get_manifest(programme_id)
                cache_entry["updated"] = datetime.now()
        return cache_entry["content"]

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
