from enum import Enum
from starlette.config import Config as ServerConfig


class DatabaseType(Enum):
    IN_MEMORY = "in_memory"
    SUPABASE = "supabase"


class Config:
    config: ServerConfig = ServerConfig()

    LOG_LEVEL = config("LOG_LEVEL", cast=str, default="INFO")
    BYPASS_OAUTH_PROXY = config("BYPASS_OAUTH_PROXY", cast=bool, default=False)
    DEFAULT_USER = config("DEV_USER", cast=str, default="default@default")
    DEFAULT_REDIRECTION = config(
        "DEFAULT_REDIRECTION", cast=str, default="https://www.chiquitoipsum.com/"
    )
    STORAGE_FLUSH_DIR = config("STORAGE_FLUSH_DIR", cast=str, default="./data")
    STORAGE_FLUSH_FILE = config("STORAGE_FLUSH_FILE", cast=str, default="golynx.db")
    STORAGE_FLUSH_PERIOD_SECONDS = config(
        "STORAGE_FLUSH_PERIOD_SECONDS", cast=int, default=10
    )
    DATABASE = config("DATABASE", cast=DatabaseType, default=DatabaseType.IN_MEMORY)
    SUPABASE_URL = config("SUPABASE_URL", cast=str, default="https://lol.supabase.co")
    SUPABASE_KEY = config("SUPABASE_KEY", cast=str, default="lol")
