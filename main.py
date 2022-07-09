import logging

from jivago.jivago_application import JivagoApplication
import ohdieux

app = JivagoApplication(ohdieux)

if __name__ == '__main__':
    app.run_dev(host="0.0.0.0",logging_level=logging.DEBUG)
