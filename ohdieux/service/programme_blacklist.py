import logging

from jivago.inject.annotation import Component, Singleton
from jivago.lang.annotations import Inject
from jivago.lang.stream import Stream
from ohdieux.config import Config


@Component
@Singleton
class ProgrammeBlacklist(object):

    @Inject
    def __init__(self, config: Config):
        self._blacklist = Stream(config.programme_blacklist).toSet()
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.info(f"Using programme blacklist {self._blacklist}.")

    def is_blacklisted(self, programme_id: int) -> bool:
        return str(programme_id) in self._blacklist
