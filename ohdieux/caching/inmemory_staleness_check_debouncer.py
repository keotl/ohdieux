import threading
from datetime import datetime, timedelta

from jivago.inject.annotation import Component, Singleton
from jivago.lang.annotations import Inject, Override
from ohdieux.caching.staleness_check_debouncer import StalenessCheckDebouncer
from ohdieux.config import Config


@Component
@Singleton
class InmemoryStalenessCheckDebouncer(StalenessCheckDebouncer):

    @Inject
    def __init__(self, config: Config):
        self._content = {}
        self._lock = threading.Lock()
        self._check_delay = timedelta(seconds=config.recheck_interval_s)

    @Override
    def set_last_checked_time(self, programme_id: int):
        with self._lock:
            self._content[programme_id] = datetime.now()

    @Override
    def should_check_again(self, programme_id: int) -> bool:
        with self._lock:
            if programme_id not in self._content:
                return True
            return datetime.now() > self._content[programme_id] + self._check_delay
