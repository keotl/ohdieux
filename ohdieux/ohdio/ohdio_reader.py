from jivago.inject.annotation import Component
from jivago.lang.annotations import Inject, Override
from ohdieux.model.programme import Programme
from ohdieux.ohdio.ohdio_api import OhdioApi
from ohdieux.ohdio.ohdio_programme_response_proxy import \
    OhdioProgrammeResponseProxy
from ohdieux.service.programme_fetching_service import ProgrammeFetchingService


@Component
class OhdioReader(ProgrammeFetchingService):

    @Inject
    def __init__(self, api: OhdioApi):
        self._api = api

    @Override
    def fetch_programme(self, programme_id: str) -> Programme:
        return self.query(programme_id, False)

    def query(self, programme_id: str, reverse_segments: bool) -> Programme:
        return OhdioProgrammeResponseProxy(self._api, programme_id,
                                           reverse_segments)
