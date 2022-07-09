import logging
import os.path

from jivago.config.production_jivago_context import ProductionJivagoContext
from jivago.config.router.router_builder import RouterBuilder
from jivago.jivago_application import JivagoApplication
from jivago.wsgi.routing.routing_rule import RoutingRule
from jivago.wsgi.routing.serving.static_file_routing_table import StaticFileRoutingTable

import ohdieux
import ohdieux.views

logging.getLogger().setLevel(logging.INFO)


class Context(ProductionJivagoContext):

    def create_router_config(self) -> RouterBuilder:
        return super().create_router_config().add_rule(RoutingRule("/static/", StaticFileRoutingTable(
            os.path.dirname(ohdieux.views.__file__), allowed_extensions=[".png"])))


application = JivagoApplication(ohdieux, context=Context)

if __name__ == '__main__':
    application.run_dev(host="0.0.0.0", logging_level=logging.DEBUG)
