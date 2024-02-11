import asyncio
import logging
import traceback

import redis
from jivago.inject.annotation import Component
from jivago.lang.annotations import Inject
from ohdieux.caching.redis_adapter import RedisAdapter
from ohdieux.ohdio.asyncio_programme_fetcher import AsyncioProgrammeFetcher


@Component
class AsyncioRedisRefreshListener(object):

    @Inject
    def __init__(self, redis: RedisAdapter, fetcher: AsyncioProgrammeFetcher):
        self._redis = redis
        self._logger = logging.getLogger(self.__class__.__name__)
        self._should_stop = False
        self._fetcher = fetcher

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
            except Exception as e:
                self._logger.error(
                    f"Uncaught exception in redis listener. Restarting in 10 seconds...",
                    traceback.format_exc())
                await asyncio.sleep(10)
                continue

    async def _do_refresh(self, programme_id: int) -> None:
        try:
            result = await self._fetcher.fetch_entire_programme_async(programme_id)
            self._redis.set(programme_id, result)
        except Exception as e:
            self._logger.error(
                f"Uncaught exception while refreshing programme {programme_id} {e}")
