import logging
import os
import os.path

from jivago.jivago_application import JivagoApplication

import ohdieux
from ohdieux.config.context import Context

LOG_LEVEL = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR
}
logging.getLogger().setLevel(
    LOG_LEVEL.get(os.environ.get("LOG_LEVEL", "INFO"), logging.INFO))

application = JivagoApplication(ohdieux, context=Context)

if __name__ == '__main__':
    application.run_dev(host="0.0.0.0", logging_level=logging.DEBUG)
