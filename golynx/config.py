from starlette.config import Config as ServerConfig

class Config:
    config: ServerConfig = ServerConfig()

    LOG_LEVEL = config('LOG_LEVEL', cast=str, default='INFO')
    DEV_MODE = config('DEV', cast=bool, default=False)
    STORAGE_FLUSH_DIR = config('STORAGE_FLUSH_DIR', cast=str, default='./data')
    STORAGE_FLUSH_FILE = config('STORAGE_FLUSH_FILE', cast=str, default='golynx.db')