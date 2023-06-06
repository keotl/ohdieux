import abc
from typing import Optional

from ohdieux.model.programme import Programme


class ProgrammeCache(abc.ABC):

    @abc.abstractmethod
    def get(self, programme_id: int) -> Optional[Programme]:
        raise NotImplementedError

    @abc.abstractmethod
    def set(self, programme_id: int, programme: Programme):
        raise NotImplementedError
