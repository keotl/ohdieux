from jivago.inject.annotation import Component
from ohdieux.ohdio.ohdio_show_response_proxy import OhdioProgrammeResponseProxy


@Component
class OhdioReader(object):

    def query(self, show_id: str) -> OhdioProgrammeResponseProxy:
        return OhdioProgrammeResponseProxy(show_id)
