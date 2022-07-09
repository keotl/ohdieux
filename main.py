import logging

from jivago.jivago_application import JivagoApplication
import ohdieux

logging.getLogger().setLevel(logging.INFO)
application = JivagoApplication(ohdieux)

if __name__ == '__main__':
    application.run_dev(host="0.0.0.0", logging_level=logging.DEBUG)
