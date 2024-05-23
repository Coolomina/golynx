import logging
import pickle

from golynx.models.domain.golink import Golink
from golynx.infrastructure.storage.storage import Storage

logger = logging.getLogger("infrastructure/database")

class Database:
    default_redirection = Golink(link='default', redirection='https://www.chiquitoipsum.com/', created_by='pepe')
    
    def __init__(self) -> None:
        pass
    
    def initialize(self, storage: Storage):
        self.storage = storage
        logger.info("Initializing database...")
        try:
            self._data = pickle.loads(self.storage.get())
        except:
            self._data = {}
        return self
    
    def get(self, link: str) -> Golink:
        return self._data.get(link, self.default_redirection)
    
    def set(self, golink: Golink):
        self._data[golink.link] = golink
    
    def delete(self, link: str):
        del self._data[link]
    
    def get_all(self):
        return self._data
    
    def flush(self):
        data = pickle.dumps(self._data)
        self.storage.write(data)