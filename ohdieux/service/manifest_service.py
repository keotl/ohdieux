from typing import NamedTuple

from jivago.inject.annotation import Component
from jivago.lang.annotations import Inject
from ohdieux.caching.invalidation_strategy import InvalidationStrategy
from ohdieux.caching.programme_cache import ProgrammeCache
from ohdieux.communication.programme_refresh_notifier import \
    ProgrammeRefreshNotifier
from ohdieux.model.programme import Programme
from ohdieux.service.programme_fetching_service import ProgrammeFetchingService
from ohdieux.transform.reverse_episode_segments import reverse_episode_segments


class ProgrammeResponse(NamedTuple):
    programme: Programme
    should_cache: bool


@Component
class ManifestService(object):

    @Inject
    def __init__(self, cache: ProgrammeCache,
                 invalidation: InvalidationStrategy,
                 refresh: ProgrammeRefreshNotifier,
                 fetcher: ProgrammeFetchingService):
        self._cache = cache
        self._invalidation = invalidation
        self._refresh = refresh
        self._fetcher = fetcher

    def generate_podcast_manifest(self, programme_id: int,
                                  reverse_segments: bool) -> ProgrammeResponse:
        programme = self._cache.get(programme_id)
        should_cache = True
        if self._invalidation.should_refresh(programme_id, programme):
            self._refresh.notify_refresh(programme_id)

        if programme is None:
            programme = self._fetcher.fetch_slim_programme(programme_id)
            should_cache = False

        if reverse_segments:
            programme = reverse_episode_segments(programme)

        return ProgrammeResponse(programme, should_cache)
