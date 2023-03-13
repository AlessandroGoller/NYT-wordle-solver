from functools import lru_cache

from app.config import Config


@lru_cache()
def get_settings():  # type: ignore
    return Config()
