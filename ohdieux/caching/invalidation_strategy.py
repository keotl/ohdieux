import threading
from datetime import datetime, timedelta
from typing import Dict

from jivago.inject.annotation import Component, Singleton
from jivago.lang.annotations import Inject
from ohdieux.config import Config
from ohdieux.model.programme import Programme
from ohdieux.service.programme_fetching_service import ProgrammeFetchingService


@Singleton
@Component
class InvalidationStrategy(object):

    @Inject
    def __init__(self, fetcher: ProgrammeFetchingService, config: Config):
        self._fetcher = fetcher
        self._forced_cache_refresh_delay = config.cache_refresh_delay_s
        self._lock = threading.Lock()
        self._last_checked: Dict[int, datetime] = {}
        self._check_delay = timedelta(minutes=5)

    def should_refresh(self, programme_id: int, programme: Programme) -> bool:
        if datetime.now() > programme.build_date + timedelta(
                seconds=self._forced_cache_refresh_delay):
            return True

        with self._lock:
            last_checked = self._last_checked.get(programme_id)
            if last_checked and datetime.now(
            ) < last_checked + self._check_delay:
                return False
            return self._check_stale(programme_id, programme)

    def _check_stale(self, programme_id: int, programme: Programme) -> bool:
        newest_episode = self._fetcher.fetch_newest_episode(programme_id)
        if newest_episode is None:
            # Some transient error most likely. Let's wait.
            stale = False
        if len(programme.episodes) == 0:
            stale = True
        elif len(programme.episodes) > 0:
            stale = newest_episode.media[0].media_url != programme.episodes[
                0].media[0].media_url
        else:
            stale = newest_episode.title != programme.programme.title
        self._last_checked[programme_id] = datetime.now()
        return stale
