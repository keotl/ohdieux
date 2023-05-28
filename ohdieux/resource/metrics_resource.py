import json

from jivago.lang.annotations import Inject
from jivago.wsgi.annotations import Resource
from jivago.wsgi.methods import GET
from ohdieux.caching.inmemory_programme_cache import InmemoryProgrammeCache
from ohdieux.caching.programme_cache import ProgrammeCache
from ohdieux.caching.redis_adapter import RedisAdapter
from ohdieux.communication.in_process_refresh_notifier import \
    InProcessRefreshNotifier
from ohdieux.communication.programme_refresh_notifier import \
    ProgrammeRefreshNotifier


@Resource("/_metrics")
class MetricsResource(object):

    @Inject
    def __init__(self, notifier: ProgrammeRefreshNotifier,
                 cache: ProgrammeCache):
        self._notifier = notifier
        self._cache = cache

    @GET
    def get_metrics(self):
        res = {}
        if isinstance(self._notifier, InProcessRefreshNotifier):
            res["pending"] = [x for x in self._notifier._pending]
        if isinstance(self._cache, InmemoryProgrammeCache):
            res["cached"] = {
                programme_id: p.build_date
                for programme_id, p in self._cache._content.items()
            }
        if isinstance(self._notifier, RedisAdapter):
            res["pending"] = json.loads(
                (self._notifier._connection.get("pending")
                 or b"[]").decode("utf-8"))
        return res
