import abc

class Storage(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get(self) -> bytes:
        raise NotImplementedError

    @abc.abstractmethod
    def write(self, data: bytes):
        raise NotImplementedError    