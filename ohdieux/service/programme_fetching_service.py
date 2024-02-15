import abc
from typing import Optional

from ohdieux.model.episode_descriptor import EpisodeDescriptor
from ohdieux.model.programme import Programme


class ProgrammeFetchingService(object):

    @abc.abstractmethod
    def fetch_programme(self, programme_id: int) -> Programme:
        raise NotImplementedError

    @abc.abstractmethod
    def fetch_slim_programme(self, programme_id: int) -> Programme:
        """Serves a version of the programme while waiting for the initial scraping."""
        raise NotImplementedError

    @abc.abstractmethod
    def fetch_newest_episode(self, programme_id: int) -> Optional[EpisodeDescriptor]:
        raise NotImplementedError


class ProgrammeNotFoundException(Exception):
    pass
