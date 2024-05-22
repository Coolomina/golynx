import asyncio
from ..infrastructure.database import Database

class DataFlusher:
    def __init__(self, database: Database) -> None:
        self.database = database
        self.loop = asyncio.get_event_loop()
    
    async def run(self):
        while self.loop.is_running:
            self.database.flush()
            await asyncio.sleep(1) # Config

    def stop(self):
        self.database.flush()