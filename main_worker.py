import asyncio
import logging
import signal

from main import application
from ohdieux.caching.refreshing.asyncio_redis_refresh_listener import \
    AsyncioRedisRefreshListener


async def main():
    _logger.info("Starting fetcher worker.")
    refresh_listener = application.serviceLocator.get(AsyncioRedisRefreshListener)
    await refresh_listener.run_refresher()


def graceful_exit(signum, frame):
    _logger.info(f"Received shutdown signal. Terminating... {signum}")
    refresh_listener = application.serviceLocator.get(AsyncioRedisRefreshListener)
    refresh_listener._should_stop = True
    application.cleanup(signum, frame)


_logger = logging.getLogger("main_worker")
if __name__ == '__main__':
    signal.signal(signal.SIGINT, graceful_exit)
    signal.signal(signal.SIGTERM, graceful_exit)
    asyncio.run(main())
