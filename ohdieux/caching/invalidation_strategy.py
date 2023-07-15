import logging
from datetime import datetime, timedelta
from typing import Optional

from jivago.inject.annotation import Component
from jivago.lang.annotations import Inject
from ohdieux.caching.staleness_check_debouncer import StalenessCheckDebouncer
from ohdieux.config import Config
from ohdieux.model.episode_descriptor import EpisodeDescriptor
from ohdieux.model.programme import Programme
from ohdieux.service.programme_fetching_service import ProgrammeFetchingService


@Component
class InvalidationStrategy(object):

    @Inject
    def __init__(self, fetcher: ProgrammeFetchingService, config: Config,
                 debouncer: StalenessCheckDebouncer):
        self._fetcher = fetcher
        self._forced_cache_refresh_delay = config.cache_refresh_delay_s
        self._debouncer = debouncer
        self._logger = logging.getLogger(self.__class__.__name__)

    def should_refresh(self, programme_id: int,
                       programme: Optional[Programme]) -> bool:
        if programme is None:
            return True
        if datetime.now() > programme.build_date + timedelta(
                seconds=self._forced_cache_refresh_delay):
            return True

        if self._debouncer.should_check_again(programme_id):
            return self._check_stale(programme_id, programme)

        return False

    def _check_stale(self, programme_id: int, programme: Programme) -> bool:
        self._logger.info(f"Checking staleness for programme {programme_id}.")
        newest_episode = self._fetcher.fetch_newest_episode(programme_id)
        if newest_episode is None:
            # Likely some transient error. Let's wait.
            stale = False
        elif len(programme.episodes) == 0:
            stale = True
        else:
            stale = _first_url(newest_episode) != _first_url(
                programme.episodes[0])
            if not _first_url(newest_episode):
                self._logger.warning(
                    f"Got no URL for newest episode {programme_id} {newest_episode}.")

        if not stale:
            self._debouncer.set_last_checked_time(programme_id)

        return stale


def _first_url(episode: Optional[EpisodeDescriptor]) -> str:
    if episode is None:
        return ""
    if not episode.media:
        return ""

    return episode.media[0].media_url
