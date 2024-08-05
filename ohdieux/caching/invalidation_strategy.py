import logging
from datetime import datetime, timedelta
from typing import Optional

from jivago.inject.annotation import Component
from jivago.lang.annotations import Inject
from jivago.lang.stream import Stream
from ohdieux.caching.refresh_whitelist import RefreshWhitelist
from ohdieux.caching.staleness_check_debouncer import StalenessCheckDebouncer
from ohdieux.config import Config
from ohdieux.model.episode_descriptor import EpisodeDescriptor
from ohdieux.model.programme import Programme, ProgrammeSummary
from ohdieux.service.programme_blacklist import ProgrammeBlacklist
from ohdieux.service.programme_fetching_service import ProgrammeFetchingService


@Component
class InvalidationStrategy(object):

    @Inject
    def __init__(self, fetcher: ProgrammeFetchingService, config: Config,
                 debouncer: StalenessCheckDebouncer, whitelist: RefreshWhitelist,
                 blacklist: ProgrammeBlacklist):
        self._fetcher = fetcher
        self._forced_cache_refresh_delay = config.cache_refresh_delay_s
        self._debouncer = debouncer
        self._whitelist = whitelist
        self._blacklist = blacklist
        self._logger = logging.getLogger(self.__class__.__name__)

    def should_refresh(self, programme_id: int, programme: Optional[Programme]) -> bool:
        if not self._whitelist.allow_refresh(
                str(programme_id)) or self._blacklist.is_blacklisted(programme_id):
            return False

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
        summary = self._fetcher.fetch_programme_summary(programme_id)
        stale = _is_stale(programme, summary)

        self._debouncer.set_last_checked_time(programme_id)

        return stale


def _is_stale(old: Programme, new: Optional[ProgrammeSummary]):
    if new is None or new["episodes"] == 0:
        return False

    # oldest_to_newest, appear to mostly be short programmes
    if old.ordering == "oldest_to_newest" and len(old.episodes) < new["episodes"]:
        return True

    # Short programmes that we can refetch quickly
    if len(old.episodes) < new["episodes"] < 50:
        return True

    # Default newest_to_oldest logic, check that the first episode is different.
    latest_old_episode = old.episodes[0]
    new_urls = list(map(lambda m: m.media_url, new["first_episodes"][0].media))
    old_urls = Stream(latest_old_episode.media).map(lambda m: m.media_url).toList()

    return (new_urls != old_urls
            or new["first_episodes"][0].title != latest_old_episode.title
            or new["first_episodes"][0].description != latest_old_episode.description)
