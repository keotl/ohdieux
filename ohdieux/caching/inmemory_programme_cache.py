import threading
from typing import Optional

from jivago.inject.annotation import Component, Singleton
from jivago.lang.annotations import Override
from ohdieux.caching.programme_cache import ProgrammeCache
from ohdieux.model.programme import Programme


@Component
@Singleton
class InmemoryProgrammeCache(ProgrammeCache):

    def __init__(self):
        self._lock = threading.Lock()
        self._content = {}

    @Override
    def get(self, programme_id: int) -> Optional[Programme]:
        with self._lock:
            return self._content.get(programme_id)

    @Override
    def set(self, programme_id: int, programme: Programme):
        with self._lock:
            self._content[programme_id] = programme
