from ..infrastructure.database import Database
from ..models.domain.golink import Golink

class LinkManager:
    def __init__(self, database: Database) -> None:
        self.database = database
    
    def handle_redirection(self, link: str) -> str:
        self.database.increment(link)
        return self.database.get(link).redirection
    
    def handle_update(self, golink: Golink):
        self.database.set(golink)
    
    def handle_delete(self, link: str):
        self.database.delete(link)
    
    def handle_get_all(self):
        return self.database.get_all()