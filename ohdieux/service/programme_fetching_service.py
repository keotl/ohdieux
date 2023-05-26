import abc

from ohdieux.model.programme import Programme


class ProgrammeFetchingService(object):

    @abc.abstractmethod
    def fetch_programme(self, programme_id: str) -> Programme:
        raise NotImplementedError
