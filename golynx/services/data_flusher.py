import asyncio
from ..infrastructure.database.base import BaseDatabase
from ..config import Config


class DataFlusher:
    def __init__(self, database: BaseDatabase) -> None:
        self.database = database
        self.loop = asyncio.get_event_loop()

    async def run(self):
        while self.loop.is_running:
            self.database.flush()
            await asyncio.sleep(Config.STORAGE_FLUSH_PERIOD_SECONDS)

    def stop(self):
        self.database.flush()
