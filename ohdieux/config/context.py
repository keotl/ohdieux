import os.path

import ohdieux
import ohdieux.views
from jivago.config.production_jivago_context import ProductionJivagoContext
from jivago.config.router.filtering.filtering_rule import FilteringRule
from jivago.config.router.router_builder import RouterBuilder
from jivago.config.startup_hooks import PostInit, PreInit
from jivago.event.config.annotations import EventHandlerClass
from jivago.inject.annotation import Provider
from jivago.inject.service_locator import ServiceLocator
from jivago.lang.annotations import BackgroundWorker, Inject, Override
from jivago.lang.runnable import Runnable
from jivago.scheduling.annotations import Duration, Scheduled
from jivago.wsgi.routing.routing_rule import RoutingRule
from jivago.wsgi.routing.serving.static_file_routing_table import \
    StaticFileRoutingTable
from ohdieux.caching.inmemory_programme_cache import InmemoryProgrammeCache
from ohdieux.caching.inmemory_staleness_check_debouncer import \
    InmemoryStalenessCheckDebouncer
from ohdieux.caching.programme_cache import ProgrammeCache
from ohdieux.caching.redis_adapter import (RedisAdapter, RedisPendingQueueJanitor,
                                           RedisRefreshListener)
from ohdieux.caching.redis_staleness_check_debouncer import \
    RedisStalenessCheckDebouncer
from ohdieux.caching.staleness_check_debouncer import StalenessCheckDebouncer
from ohdieux.communication.in_process_refresh_notifier import \
    InProcessRefreshNotifier
from ohdieux.communication.programme_refresh_notifier import \
    ProgrammeRefreshNotifier
from ohdieux.config import Config
from ohdieux.ohdio.asyncio_programme_fetcher import AsyncioProgrammeFetcher
from ohdieux.service.programme_fetching_service import ProgrammeFetchingService
from ohdieux.util.wsgi.static_cache_headers_filter import \
    StaticCacheHeadersFilter
from ohdieux.util.wsgi.static_file_mimetype_fix_filter import \
    StaticFileMimetypeFixFilter


class Context(ProductionJivagoContext):

    @Override
    def create_router_config(self) -> RouterBuilder:
        return super().create_router_config() \
            .add_rule(
                RoutingRule("/static/",
                            StaticFileRoutingTable(
                                os.path.dirname(ohdieux.views.__file__),
                                allowed_extensions=[".png", ".js"]))) \
            .add_rule(FilteringRule("/static/*", [StaticCacheHeadersFilter, StaticFileMimetypeFixFilter])) \
            .add_rule(
                RoutingRule("/",
                            StaticFileRoutingTable(
                                os.path.dirname(ohdieux.views.__file__),
                                allowed_extensions=[".ico"])))

    @Override
    def configure_service_locator(self):
        self.service_locator().bind(ProgrammeFetchingService, AsyncioProgrammeFetcher)
        # self.service_locator().bind(ProgrammeFetchingService, OhdioProgrammeFetcher)
        return super().configure_service_locator()


@Provider
def configure_cache(config: Config, service_locator: ServiceLocator) -> ProgrammeCache:
    if config.cache_strategy == "memory":
        return service_locator.get(InmemoryProgrammeCache)
    elif config.cache_strategy == "redis":
        return service_locator.get(RedisAdapter)
    raise Exception(f"Unsupported caching strategy {config.cache_strategy}.")


@Provider
def configure_staleness_check(
        config: Config, service_locator: ServiceLocator) -> StalenessCheckDebouncer:
    if config.cache_strategy == "memory":
        return service_locator.get(InmemoryStalenessCheckDebouncer)
    elif config.cache_strategy == "redis":
        return service_locator.get(RedisStalenessCheckDebouncer)
    raise Exception(f"Unsupported caching strategy {config.cache_strategy}.")


@Provider
def configure_notifier(config: Config,
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
        self.run_worker_process = config.run_fetcher_worker

    @Override
    def run(self):
        if self.cache_strategy == "redis":
            EventHandlerClass(RedisAdapter)
            if self.run_worker_process:
                BackgroundWorker(RedisRefreshListener)
            PostInit(RedisPendingQueueJanitor)
            Scheduled(every=Duration.DAY)(RedisPendingQueueJanitor)
        elif self.cache_strategy == "memory":
            EventHandlerClass(InProcessRefreshNotifier)
