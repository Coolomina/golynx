import logging

from golynx.infrastructure.storage.disk import Disk
from golynx.infrastructure.storage.storage import Storage

logger = logging.getLogger("infrastructure/database")

class Database:
    default_redirection = "https://www.chiquitoipsum.com/"
    
    def __init__(self) -> None:
        pass
    
    def initialize(self, storage: Storage):
        self.storage = storage
        logger.info("Initializing database...")
        self._data = self.storage.get()
        return self
    
    def get(self, link: str) -> str:
        return self._data.get(link, self.default_redirection)
    
    def set(self, link: str, redirection: str):
        self._data[link] = redirection
    
    def delete(self, link: str):
        del self._data[link]
    
    def get_all(self):
        return self._data
    
    def flush(self):
        self.storage.write(self._data)