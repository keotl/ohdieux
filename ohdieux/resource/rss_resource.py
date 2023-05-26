import logging
from email.utils import formatdate
from typing import List, NamedTuple

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
    def get_manifest(self, programme_id: QueryParam[int], reverse: bool):
        programme = self._manifest_service.generate_podcast_manifest(
            int(str(programme_id)), bool(reverse))
        rendered_episodes = Stream(programme.episodes).map(
            render_episode).flat().toList()  # type: ignore
        return RenderedView(
            "manifest.xml", {
                "programme": programme.programme,
                "episodes": rendered_episodes,
                "now": formatdate(float(programme.build_date.strftime("%s")))
            },
            content_type="text/xml")

    @HEAD
    def headers(self):
        return ""


class RenderedEpisode(NamedTuple):
    title: str
    description: str
    guid: str
    date: str
    duration: int
    media: MediaDescriptor


def render_episode(episode: EpisodeDescriptor) -> List[RenderedEpisode]:
    res = []
    for stream in episode.media:
        res.append(
            RenderedEpisode(title=episode.title,
                            description=episode.description,
                            guid=stream.media_url,
                            date=formatdate(float(
                                episode.date.strftime("%s"))),
                            duration=episode.duration,
                            media=stream))
    return res
