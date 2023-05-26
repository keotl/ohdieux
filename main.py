import logging
import os.path

from jivago.config.production_jivago_context import ProductionJivagoContext
from jivago.config.router.router_builder import RouterBuilder
from jivago.jivago_application import JivagoApplication
from jivago.lang.annotations import Override
from jivago.wsgi.routing.routing_rule import RoutingRule
from jivago.wsgi.routing.serving.static_file_routing_table import \
    StaticFileRoutingTable

import ohdieux
import ohdieux.views
from ohdieux.caching.inmemory_programme_cache import InmemoryProgrammeCache
from ohdieux.caching.programme_cache import ProgrammeCache
from ohdieux.communication.in_process_refresh_notifier import \
    InProcessRefreshNotifier
from ohdieux.communication.programme_refresh_notifier import \
    ProgrammeRefreshNotifier
from ohdieux.ohdio.ohdio_programme_fetcher import OhdioProgrammeFetcher
from ohdieux.service.programme_fetching_service import ProgrammeFetchingService

LOG_LEVEL = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR
}
logging.getLogger().setLevel(
    LOG_LEVEL.get(os.environ.get("LOG_LEVEL", "INFO"), logging.INFO))


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
        self.service_locator().bind(ProgrammeCache, InmemoryProgrammeCache)
        self.service_locator().bind(ProgrammeFetchingService,
                                    OhdioProgrammeFetcher)
        self.service_locator().bind(ProgrammeRefreshNotifier,
                                    InProcessRefreshNotifier)

        return super().configure_service_locator()


application = JivagoApplication(ohdieux, context=Context)

if __name__ == '__main__':
    application.run_dev(host="0.0.0.0", logging_level=logging.DEBUG)
