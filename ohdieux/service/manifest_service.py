from typing import NamedTuple

from jivago.inject.annotation import Component
from jivago.lang.annotations import Inject
from ohdieux.caching.programme_cache import ProgrammeCache
from ohdieux.communication.programme_refresh_notifier import \
    ProgrammeRefreshNotifier
from ohdieux.model.programme import Programme
from ohdieux.service.programme_fetching_service import ProgrammeFetchingService


class ProgrammeResponse(NamedTuple):
    programme: Programme
    should_cache: bool


@Component
class ManifestService(object):

    @Inject
    def __init__(self, cache: ProgrammeCache, refresh: ProgrammeRefreshNotifier,
                 fetcher: ProgrammeFetchingService):
        self._cache = cache
        self._refresh = refresh
        self._fetcher = fetcher

    def generate_podcast_manifest(self, programme_id: int) -> ProgrammeResponse:
        programme = self._cache.get(programme_id)
        should_cache = True

        if programme is None:
            programme = self._fetcher.fetch_slim_programme(programme_id)
            should_cache = False

        self._refresh.notify_refresh(programme_id)

        return ProgrammeResponse(programme, should_cache)
