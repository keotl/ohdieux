import asyncio
import logging
import traceback
from datetime import datetime

import redis
from jivago.event.synchronous_event_bus import SynchronousEventBus
from jivago.inject.annotation import Component
from jivago.lang.annotations import Inject
from ohdieux.caching.invalidation_strategy import InvalidationStrategy
from ohdieux.caching.programme_cache import ProgrammeCache
from ohdieux.caching.redis_adapter import RedisAdapter
from ohdieux.ohdio.asyncio_programme_fetcher import AsyncioProgrammeFetcher
from ohdieux.ohdio.programme_type import infer_programme_type


@Component
class AsyncioRedisRefreshListener(object):

    @Inject
    def __init__(self, redis: RedisAdapter, fetcher: AsyncioProgrammeFetcher,
                 event_bus: SynchronousEventBus, invalidation: InvalidationStrategy,
                 cache: ProgrammeCache):
        self._redis = redis
        self._logger = logging.getLogger(self.__class__.__name__)
        self._should_stop = False
        self._fetcher = fetcher
        self._bus = event_bus
        self._cache = cache
        self._invalidation = invalidation

    async def run_refresher(self):
        while not self._should_stop:
            try:
                self._redis._pubsub.subscribe("refresh_programme")
                for message in self._redis._pubsub.listen():
                    if message is None:
                        continue
                    programme_id = int(message.get("data"))
                    if self._redis._mark_pending_and_should_send_refresh_message(
                            programme_id):
                        await self._do_refresh(programme_id)
            except redis.exceptions.RedisError as e:
                self._logger.warning(
                    f"Redis connection closed. Restarting listener in 10 seconds... {e}"
                )
                await asyncio.sleep(10)
                continue
            except Exception:
                self._logger.error(
                    "Uncaught exception in redis listener. Restarting in 10 seconds...",
                    traceback.format_exc())
                await asyncio.sleep(10)
                continue

    async def _do_refresh(self, programme_id: int) -> None:
        try:
            if not self._invalidation.should_refresh(programme_id,
                                                     self._redis.get(programme_id)):
                self._logger.debug(
                    f"Skipping refreshing programme {programme_id} because it is not stale."
                )
                return

            start = datetime.now()
            cached = self._cache.get(programme_id)

            if cached is not None and len(
                    cached.episodes) > 0 and cached.ordering != "oldest_to_newest":

                self._logger.info(f"Refreshing programme {programme_id} incrementally.")
                result = await self._fetcher.fetch_programme_incremental_async(
                    programme_id, cached)
                programme_summary = self._fetcher.fetch_programme_summary(
                    programme_id, infer_programme_type(result))
                missing_episodes = programme_summary["episodes"] - len(result.episodes)
                if missing_episodes / (programme_summary["episodes"] or 1) > 0.1:
                    self._logger.error(
                        f"Programme {programme_id} is missing {missing_episodes}/{programme_summary['episodes']} episodes. Consider clearing cache manually."
                    )
                    if programme_summary["episodes"] < 50:
                        self._logger.info(
                            f"Attempting to refetch full programme {programme_id}")
                        result = await self._fetcher.fetch_entire_programme_async(
                            programme_id)

            else:
                self._logger.info(f"Refreshing programme {programme_id}.")
                result = await self._fetcher.fetch_entire_programme_async(programme_id)

            self._redis.set(programme_id, result)
            self._logger.info(
                f"Done refreshing programme {programme_id} in {datetime.now() - start}."
            )
        except Exception as e:
            self._logger.error(
                f"Uncaught exception while refreshing programme {programme_id} {e}")
            traceback.print_exc()
        finally:
            self._bus.emit("refresh_complete", programme_id)
