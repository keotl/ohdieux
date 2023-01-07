import logging
import threading
from datetime import datetime
from email.utils import formatdate

from jivago.inject.annotation import Singleton
from jivago.lang.annotations import Inject
from jivago.lang.stream import Stream
from jivago.templating.rendered_view import RenderedView
from jivago.wsgi.annotations import Resource
from jivago.wsgi.invocation.parameters import QueryParam, OptionalQueryParam
from jivago.wsgi.methods import GET, HEAD

from ohdieux.config import Config
from ohdieux.model.episode_descriptor import EpisodeDescriptor, MediaDescriptor
from ohdieux.service.manifest_service import ManifestService


@Resource("/rss")
@Singleton
class RssResource(object):

    @Inject
    def __init__(self, manifest_service: ManifestService, config: Config):
        self._manifest_service = manifest_service
        self._cache = {}
        self._lock = threading.Lock()
        self._cache_refresh_delay = config.cache_refresh_delay_s
        self._logger = logging.getLogger(self.__class__.__name__)

    @GET
    def cached(self, programme_id: QueryParam[str], reverse: OptionalQueryParam[str]):
        reverse = reverse in ("true", "True", "1")
        with self._lock:
            if (programme_id, reverse) not in self._cache:
                self._cache[(programme_id, reverse)] = {"lock": threading.Lock(), "updated": datetime.min, "content": None}

        cache_entry = self._cache[(programme_id, reverse)]
        with cache_entry["lock"]:
            if (datetime.now() - cache_entry["updated"]).total_seconds() > self._cache_refresh_delay:
                self._logger.info(f"Refreshing programme {programme_id}, reverse={reverse}.")
                start_time = datetime.now()
                cache_entry["content"] = self.get_manifest(programme_id, reverse)
                cache_entry["updated"] = datetime.now()
                self._logger.info(f"Completed refresh of programme {programme_id} in {datetime.now() - start_time}.")
        return cache_entry["content"]

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
