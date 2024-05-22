import logging
import os
import sys

LOG_LEVEL = os.environ.get("LOGLEVEL", "INFO").upper()

def initialize_logger(
    logger_name: str = "golynx", log_level: str = LOG_LEVEL
) -> logging.Logger:
    stderr_handler = logging.StreamHandler(stream=sys.stderr)
    handlers: list[logging.Handler] = [stderr_handler]

    logging.basicConfig(
        level=log_level, format="[%(asctime)s] [%(name)s] %(levelname)s - %(message)s", handlers=handlers
    )
    return logging.getLogger(logger_name.upper())
