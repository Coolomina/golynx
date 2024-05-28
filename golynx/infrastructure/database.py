import logging
import pickle
import threading

from golynx.models.domain.golink import Golink
from golynx.infrastructure.storage.storage import Storage

logger = logging.getLogger("infrastructure/database")

class Database:
    default_redirection = Golink(
        link='default',
        redirection='https://www.chiquitoipsum.com/',
        created_by='pepe',
    )
    
    def __init__(self) -> None:
        self.lock = threading.Lock()
    
    def initialize(self, storage: Storage):
        self.storage = storage
        logger.info("Initializing database...")
        try:
            self._data: dict[str, Golink] = pickle.loads(self.storage.get())
            logger.info(f'Initialised storage with {len(self._data)} elements')
        except:
            self._data: dict[str, Golink] = {}
        return self
    
    def get(self, link: str) -> Golink:
        return self._data.get(link, self.default_redirection)
    
    def increment(self, link: str):
        self.lock.acquire()
        try:
            self._data[link].times_used += 1
        except KeyError:
            pass
        finally:
            self.lock.release()

    def set(self, golink: Golink):
        self.lock.acquire()
        try:
            self._data[golink.link] = golink
        finally:
            self.lock.release()

    def delete(self, link: str):
        self.lock.acquire()
        try:
            del self._data[link]
        finally:
            self.lock.release()
    
    def get_all(self):
        if self._data.__len__ == 0:
            return {}
        data = {}
        for link in self._data.keys():
            data[link] = self._data[link].__dict__
        return data
    
    def flush(self):
        data = pickle.dumps(self._data)
        self.storage.write(data)