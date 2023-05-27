import os.path

import ohdieux
import ohdieux.views
from jivago.config.production_jivago_context import ProductionJivagoContext
from jivago.config.router.router_builder import RouterBuilder
from jivago.inject.annotation import Provider
from jivago.inject.service_locator import ServiceLocator
from jivago.lang.annotations import Override
from jivago.wsgi.routing.routing_rule import RoutingRule
from jivago.wsgi.routing.serving.static_file_routing_table import \
    StaticFileRoutingTable
from ohdieux.caching.inmemory_programme_cache import InmemoryProgrammeCache
from ohdieux.caching.programme_cache import ProgrammeCache
from ohdieux.caching.redis_adapter import RedisAdapter
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
def configure_notifier(
        config: Config,
        service_locator: ServiceLocator) -> ProgrammeRefreshNotifier:
    if config.cache_strategy == "memory":
        return service_locator.get(InProcessRefreshNotifier)
    elif config.cache_strategy == "redis":
        return service_locator.get(RedisAdapter)
    raise Exception(f"Unsupported caching strategy {config.cache_strategy}.")
