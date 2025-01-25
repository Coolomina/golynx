import logging
import os
from pathlib import Path

from golynx.infrastructure.storage.storage import Storage

logger = logging.getLogger("infrastructure/storage")


class Disk(Storage):
    def __init__(
        self,
        flush_dir,
        flush_file,
    ) -> None:
        self.flush_dir = flush_dir
        self.flush_file = flush_file
        self.flush_location = f"{self.flush_dir}/{self.flush_file}"

        logger.info("Initializing storage")
        Path(self.flush_dir).mkdir(parents=True, exist_ok=True)

        if os.path.exists(self.flush_location):
            try:
                with open(self.flush_location, "r"):
                    logger.info(f"Storage initialised at {self.flush_location}")
            except:
                logger.error(
                    f"Error: The file {self.flush_location} is not a valid DB file."
                )
                raise
        else:
            logger.info(
                f"Didn't find any database at {self.flush_location}. Initializing it..."
            )
            self.write(database=bytearray())

    def get(self) -> bytes:
        with open(self.flush_location, "rb") as file:
            return file.read()

    def write(self, database: bytes):
        with open(self.flush_location, "wb") as file:
            file.write(database)
