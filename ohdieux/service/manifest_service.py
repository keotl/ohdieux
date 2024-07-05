from datetime import datetime
from typing import NamedTuple

from jivago.inject.annotation import Component
from jivago.lang.annotations import Inject
from ohdieux.caching.programme_cache import ProgrammeCache
from ohdieux.communication.programme_refresh_notifier import \
    ProgrammeRefreshNotifier
from ohdieux.model.episode_descriptor import EpisodeDescriptor, MediaDescriptor
from ohdieux.model.programme import Programme
from ohdieux.model.programme_descriptor import ProgrammeDescriptor
from ohdieux.service.programme_blacklist import ProgrammeBlacklist
from ohdieux.service.programme_fetching_service import ProgrammeFetchingService


class ProgrammeResponse(NamedTuple):
    programme: Programme
    should_cache: bool


@Component
class ManifestService(object):

    @Inject
    def __init__(self, cache: ProgrammeCache, refresh: ProgrammeRefreshNotifier,
                 fetcher: ProgrammeFetchingService, blacklist: ProgrammeBlacklist):
        self._cache = cache
        self._refresh = refresh
        self._fetcher = fetcher
        self._blacklist = blacklist

    def generate_podcast_manifest(self, programme_id: int) -> ProgrammeResponse:
        if self._blacklist.is_blacklisted(programme_id):
            return ProgrammeResponse(_blacklisted_programme, True)

        programme = self._cache.get(programme_id)
        should_cache = True

        if programme is None:
            programme = self._fetcher.fetch_slim_programme(programme_id)
            should_cache = False

        self._refresh.notify_refresh(programme_id)

        return ProgrammeResponse(programme, should_cache)


_blacklisted_programme = Programme(
    ProgrammeDescriptor(title="Programme inconnu / Unknown Programme",
                        description="",
                        author="Ohdieux",
                        link="",
                        image_url=""),
    [
        EpisodeDescriptor("Programme inconnu / Unknown Programme", "", "000000",
                          datetime(2000, 1, 1), 1, [MediaDescriptor("", "", 1)], False)
    ], datetime.now())
