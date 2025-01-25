from golynx.infrastructure.storage.storage import Storage
from golynx.models.domain.golink import Golink


class BaseDatabase:
    def __init__(self):
        pass

    def initialize(self, storage: Storage | None = None):
        pass

    def get(self, link: str) -> Golink:
        raise NotImplementedError

    def increment(self, link: str):
        raise NotImplementedError

    def set(self, golink: Golink):
        raise NotImplementedError

    def delete(self, link: str):
        raise NotImplementedError

    def update(self, link: str, golink: Golink):
        raise NotImplementedError

    def get_all(self, as_dict=True):
        raise NotImplementedError

    def flush(self):
        pass

    def truncate(self):
        raise NotImplementedError
