from jivago.inject.annotation import Component
from jivago.lang.annotations import Inject
from ohdieux.ohdio.ohdio_api import OhdioApi

from ohdieux.ohdio.ohdio_programme_response_proxy import OhdioProgrammeResponseProxy

@Component
class OhdioReader(object):

    @Inject
    def __init__(self, api: OhdioApi):
        self._api = api
        

    def query(self, programme_id: str) -> OhdioProgrammeResponseProxy:
        return OhdioProgrammeResponseProxy(self._api, programme_id)
