from datetime import datetime, timedelta
import traceback

from jivago.inject.annotation import Component
from jivago.lang.annotations import Inject, Override
from ohdieux.caching.redis_adapter import RedisAdapter
from ohdieux.caching.staleness_check_debouncer import StalenessCheckDebouncer
from ohdieux.config import Config


@Component
class RedisStalenessCheckDebouncer(StalenessCheckDebouncer):

    @Inject
    def __init__(self, redis: RedisAdapter, config: Config):
        self._redis = redis
        self._check_delay = timedelta(seconds=config.recheck_interval_s)

    @Override
    def set_last_checked_time(self, programme_id: int):
        self._redis._connection.set(f"last_checked_{programme_id}",
                                    datetime.now().isoformat())

    @Override
    def should_check_again(self, programme_id: int) -> bool:
        saved = self._redis._connection.get(f"last_checked_{programme_id}")
        if saved is None:
            return True
        try:
            return datetime.now() > datetime.fromisoformat(
                saved.decode("utf-8")) + self._check_delay
        except KeyboardInterrupt as e:
            raise e
        except Exception:
            traceback.print_exc()
            return True
