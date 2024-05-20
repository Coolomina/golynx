import logging

logger = logging.getLogger("infrastructure/database")

class Database:
    default_redirection = "https://www.chiquitoipsum.com/"
    
    def __init__(self) -> None:
        pass
    
    def initialize(self):
        logger.info("Initializing database...")
        self._data = {}
        return self
    
    def get(self, link: str) -> str:
        return self._data.get(link, self.default_redirection)
    
    def set(self, link: str, redirection: str):
        self._data[link] = redirection
    
    def delete(self, link: str):
        del self._data[link]