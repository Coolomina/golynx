from starlette.config import Config as ServerConfig

class Config:
    config: ServerConfig = ServerConfig()

    LOG_LEVEL = config('LOG_LEVEL', cast=str, default='INFO')
    BYPASS_OAUTH_PROXY = config('BYPASS_OAUTH_PROXY', cast=bool, default=False)
    DEFAULT_USER = config('DEV_USER', cast=str, default="default@default")
    STORAGE_FLUSH_DIR = config('STORAGE_FLUSH_DIR', cast=str, default='./data')
    STORAGE_FLUSH_FILE = config('STORAGE_FLUSH_FILE', cast=str, default='golynx.db')
    STORAGE_FLUSH_PERIOD_SECONDS = config('STORAGE_FLUSH_PERIOD_SECONDS', cast=int, default=10)