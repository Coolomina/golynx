from enum import Enum
from starlette.config import Config as ServerConfig


class DatabaseType(Enum):
    IN_MEMORY = "in_memory"
    SUPABASE = "supabase"


class StorageType(Enum):
    DISK = "disk"
    S3 = "s3"
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
    STORAGE = config("STORAGE", cast=StorageType, default=StorageType.DISK)
    STORAGE_S3_BUCKET = config("STORAGE_S3_BUCKET", cast=str, default="golynx")
    STORAGE_S3_AWS_ACCESS_KEY_ID = config(
        "STORAGE_S3_AWS_ACCESS_KEY_ID", cast=str, default="lol"
    )
    STORAGE_S3_AWS_SECRET_ACCESS_KEY = config(
        "STORAGE_S3_AWS_SECRET_ACCESS_KEY", cast=str, default="lol"
    )
