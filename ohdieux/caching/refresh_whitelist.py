import logging
from jivago.inject.annotation import Component
from jivago.lang.annotations import Inject
from jivago.lang.stream import Stream
from ohdieux.config import Config


@Component
class RefreshWhitelist(object):

    @Inject
    def __init__(self, config: Config):
        self._enabled = config.use_refresh_whitelist
        self._whitelist = Stream(config.refresh_whitelist).toSet()
        self._logger = logging.getLogger(self.__class__.__name__)
        if self._enabled:
            self._logger.info(f"Whitelist enabled with {self._whitelist}")

    def allow_refresh(self, programme_id: str) -> bool:
        if self._enabled:
            return programme_id in self._whitelist
        return True
