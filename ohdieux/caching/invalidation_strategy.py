import logging
from datetime import datetime, timedelta
from typing import Optional

from jivago.inject.annotation import Component
from jivago.lang.annotations import Inject
from jivago.lang.stream import Stream
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

    def should_refresh(self, programme_id: int, programme: Optional[Programme]) -> bool:
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
        stale = _is_stale(programme, newest_episode)
        if not stale:
            self._debouncer.set_last_checked_time(programme_id)

        return stale


def _is_stale(old: Programme, new: Optional[EpisodeDescriptor]):
    if new is None:
        # Likely some transient error. Let's wait.
        return False
    if len(old.episodes) == 0:
        return True
    latest_old_episode = old.episodes[0]
    new_urls = Stream(new.media).map(lambda m: m.media_url).toList()
    old_urls = Stream(latest_old_episode.media).map(lambda m: m.media_url).toList()

    return (new_urls != old_urls or new.title != latest_old_episode.title
            or new.description != latest_old_episode.description)
