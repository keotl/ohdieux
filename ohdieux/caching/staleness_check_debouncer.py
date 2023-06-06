import abc


class StalenessCheckDebouncer(abc.ABC):

    @abc.abstractmethod
    def set_last_checked_time(self, programme_id: int):
        raise NotImplementedError

    @abc.abstractmethod
    def should_check_again(self, programme_id: int) -> bool:
        raise NotImplementedError
