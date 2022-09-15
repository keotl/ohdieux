import logging
from jivago.inject.annotation import Component
from jivago.lang.annotations import Inject
from ohdieux.model.programme import Programme

from ohdieux.ohdio.ohdio_reader import OhdioReader
from ohdieux.ohdio.ohdio_reader_v2 import OhdioReaderV2


@Component
class ManifestService(object):

    @Inject
    def __init__(self, ohdio_reader: OhdioReader, reader_v2: OhdioReaderV2):
        self._ohdio_reader = ohdio_reader
        self._reader_v2 = reader_v2
        self._logger = logging.getLogger(self.__class__.__name__)

    def generate_podcast_manifest(self, programme_id: str, reverse_segments: bool) -> Programme:
        for reader in [self._reader_v2, self._ohdio_reader]:
            try:
                res = reader.query(programme_id, reverse_segments)
                if res.programme is None:
                    self._logger.warning(f"Failed to generate manifest for programme {programme_id} using {reader.__class__} reader.")
                    continue
                return res
            except Exception as e:
                self._logger.warning(f"Failed to generate manifest for programme {programme_id} using {reader.__class__} reader.", e)

            return self._ohdio_reader.query(programme_id, reverse_segments)
