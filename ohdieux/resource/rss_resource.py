import logging
from email.utils import formatdate

from jivago.lang.annotations import Inject
from jivago.lang.stream import Stream
from jivago.templating.rendered_view import RenderedView
from jivago.wsgi.annotations import Resource
from jivago.wsgi.invocation.parameters import OptionalQueryParam, QueryParam
from jivago.wsgi.methods import GET, HEAD
from jivago.wsgi.request.request import Request
from jivago.wsgi.request.response import Response
from ohdieux.resource.rendering.episode_renderer import renderer
from ohdieux.service.manifest_service import ManifestService
from ohdieux.util.query_params import parse_bool


@Resource("/rss")
class RssResource(object):

    @Inject
    def __init__(self, manifest_service: ManifestService):
        self._manifest_service = manifest_service
        self._logger = logging.getLogger(self.__class__.__name__)

    @GET
    def get_manifest(self, programme_id: QueryParam[int],
                     reverse: OptionalQueryParam[str],
                     tag_segments: OptionalQueryParam[str],
                     favor_aac: OptionalQueryParam[str],
                     limit_episodes: OptionalQueryParam[str],
                     exclude_replays: OptionalQueryParam[str], request: Request):
        _reverse = parse_bool(reverse)
        _tag_segments = parse_bool(tag_segments)
        _favor_aac = parse_bool(favor_aac)
        _limit_episodes = parse_bool(limit_episodes)
        _exclude_replays = parse_bool(exclude_replays)

        self._logger.info(
            f"GET /rss?programme_id={programme_id} {request.headers['User-Agent']}")

        programme_response = self._manifest_service.generate_podcast_manifest(
            int(str(programme_id)))
        programme = programme_response.programme

        rendered_programme = renderer(tag_segments=_tag_segments,
                                      favor_aac=_favor_aac,
                                      reverse_segments=_reverse,
                                      limit_episodes=_limit_episodes,
                                      exclude_replays=_exclude_replays)(programme)

        rendered_episodes = Stream(rendered_programme.episodes).toList()

        body = RenderedView("manifest.xml", {
            "programme": programme.programme,
            "episodes": rendered_episodes,
            "now": formatdate(float(programme.build_date.strftime("%s")))
        },
                            content_type="text/xml")
        return Response(200, _response_headers(programme_response.should_cache), body)

    @HEAD
    def headers(self):
        return ""


def _response_headers(should_cache: bool) -> dict:
    if not should_cache:
        return {"Cache-Control": "no-cache"}

    return {
        "Cache-Control": "max-age=1800, stale-while-revalidate=60, stale-if-error=86400"
    }
