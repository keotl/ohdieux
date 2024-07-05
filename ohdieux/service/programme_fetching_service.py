import abc

from ohdieux.model.programme import Programme, ProgrammeSummary


class ProgrammeFetchingService(object):

    @abc.abstractmethod
    def fetch_programme(self, programme_id: int) -> Programme:
        raise NotImplementedError

    @abc.abstractmethod
    def fetch_slim_programme(self, programme_id: int) -> Programme:
        """Serves a version of the programme while waiting for the initial scraping."""
        raise NotImplementedError

    @abc.abstractmethod
    def fetch_programme_summary(self, programme_id: int) -> ProgrammeSummary:
        """For staleness checking"""
        raise NotImplementedError


class ProgrammeNotFoundException(Exception):
    pass
