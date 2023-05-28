import os.path

from jivago.config.startup_hooks import PostInit, PreInit
from jivago.event.config.annotations import EventHandlerClass
from jivago.lang.runnable import Runnable
from jivago.scheduling.annotations import Duration, Scheduled
from ohdieux.caching.inmemory_staleness_check_debouncer import InmemoryStalenessCheckDebouncer

import ohdieux
from ohdieux.caching.redis_staleness_check_debouncer import RedisStalenessCheckDebouncer
from ohdieux.caching.staleness_check_debouncer import StalenessCheckDebouncer
import ohdieux.views
from jivago.config.production_jivago_context import ProductionJivagoContext
from jivago.config.router.router_builder import RouterBuilder
from jivago.inject.annotation import Provider
from jivago.inject.service_locator import ServiceLocator
from jivago.lang.annotations import BackgroundWorker, Inject, Override
from jivago.wsgi.routing.routing_rule import RoutingRule
from jivago.wsgi.routing.serving.static_file_routing_table import \
    StaticFileRoutingTable
from ohdieux.caching.inmemory_programme_cache import InmemoryProgrammeCache
from ohdieux.caching.programme_cache import ProgrammeCache
from ohdieux.caching.redis_adapter import RedisAdapter, RedisPendingQueueJanitor, RedisRefreshListener
from ohdieux.communication.in_process_refresh_notifier import \
    InProcessRefreshNotifier
from ohdieux.communication.programme_refresh_notifier import \
    ProgrammeRefreshNotifier
from ohdieux.config import Config
from ohdieux.ohdio.ohdio_programme_fetcher import OhdioProgrammeFetcher
from ohdieux.service.programme_fetching_service import ProgrammeFetchingService


class Context(ProductionJivagoContext):

    @Override
    def create_router_config(self) -> RouterBuilder:
        return super().create_router_config().add_rule(
            RoutingRule(
                "/static/",
                StaticFileRoutingTable(os.path.dirname(ohdieux.views.__file__),
                                       allowed_extensions=[".png"])))

    @Override
    def configure_service_locator(self):
        self.service_locator().bind(ProgrammeFetchingService,
                                    OhdioProgrammeFetcher)
        self.service_locator().bind(ProgrammeRefreshNotifier,
                                    InProcessRefreshNotifier)
        return super().configure_service_locator()


@Provider
def configure_cache(config: Config,
                    service_locator: ServiceLocator) -> ProgrammeCache:
    if config.cache_strategy == "memory":
        return service_locator.get(InmemoryProgrammeCache)
    elif config.cache_strategy == "redis":
        return service_locator.get(RedisAdapter)
    raise Exception(f"Unsupported caching strategy {config.cache_strategy}.")


@Provider
def configure_staleness_check(config: Config,
                              service_locator: ServiceLocator) -> StalenessCheckDebouncer:
    if config.cache_strategy == "memory":
        return service_locator.get(InmemoryStalenessCheckDebouncer)
    elif config.cache_strategy == "redis":
        return service_locator.get(RedisStalenessCheckDebouncer)
    raise Exception(f"Unsupported caching strategy {config.cache_strategy}.")


@Provider
def configure_notifier(
        config: Config,
        service_locator: ServiceLocator) -> ProgrammeRefreshNotifier:
    if config.cache_strategy == "memory":
        return service_locator.get(InProcessRefreshNotifier)
    elif config.cache_strategy == "redis":
        return service_locator.get(RedisAdapter)
    raise Exception(f"Unsupported caching strategy {config.cache_strategy}.")


@PreInit
class BackgroundThreadBinder(Runnable):

    @Inject
    def __init__(self, config: Config):
        self.cache_strategy = config.cache_strategy

    @Override
    def run(self):
        if self.cache_strategy == "redis":
            EventHandlerClass(RedisAdapter)
            BackgroundWorker(RedisRefreshListener)
            PostInit(RedisPendingQueueJanitor)
            Scheduled(every=Duration.DAY)(RedisPendingQueueJanitor)
        elif self.cache_strategy == "memory":
            EventHandlerClass(InProcessRefreshNotifier)
