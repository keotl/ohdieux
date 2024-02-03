import logging
import traceback as tb
from datetime import datetime

from jivago.event.config.annotations import EventHandler, EventHandlerClass
from jivago.event.synchronous_event_bus import SynchronousEventBus
from jivago.inject.annotation import Component
from jivago.lang.annotations import Inject

from ohdieux.caching.invalidation_strategy import InvalidationStrategy
from ohdieux.caching.programme_cache import ProgrammeCache
from ohdieux.service.programme_fetching_service import (
    ProgrammeFetchingService, ProgrammeNotFoundException)


@Component
@EventHandlerClass
class ProgrammeRefresher(object):

    @Inject
    def __init__(self, fetcher: ProgrammeFetchingService,
                 cache: ProgrammeCache, event_bus: SynchronousEventBus,
                 invalidation_strategy: InvalidationStrategy):
        self._fetcher = fetcher
        self._cache = cache
        self._bus = event_bus
        self._invalidation = invalidation_strategy
        self._logger = logging.getLogger(self.__class__.__name__)

    @EventHandler("refresh_programme")
    def do_refresh(self, programme_id: int):
        try:
            if not self._invalidation.should_refresh(
                    programme_id, self._cache.get(programme_id)):
                return
            self._logger.info(f"Refreshing programme {programme_id}.")
            start = datetime.now()
            programme = self._fetcher.fetch_programme(programme_id)
            self._cache.set(programme_id, programme)
            self._logger.info(
                f"Done refreshing programme {programme_id} in {datetime.now() - start}."
            )
        except ProgrammeNotFoundException:
            self._logger.info(
                f"Could not find programme {programme_id}. Ignoring.")
        except KeyboardInterrupt as e:
            raise e
        except Exception:
            self._logger.error(
                f"Uncaught exception while refreshing programme {programme_id} {tb.format_exc()}."
            )
        finally:
            self._bus.emit("refresh_complete", programme_id)
