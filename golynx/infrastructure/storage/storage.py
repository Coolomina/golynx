import abc

class Storage(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get(self) -> dict:
        raise NotImplementedError

    @abc.abstractmethod
    def write(self, data: dict):
        raise NotImplementedError    