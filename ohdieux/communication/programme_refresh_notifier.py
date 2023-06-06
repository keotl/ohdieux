import abc


class ProgrammeRefreshNotifier(abc.ABC):

    @abc.abstractmethod
    def notify_refresh(self, programme_id: int):
        raise NotImplementedError
