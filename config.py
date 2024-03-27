import os
from functools import lru_cache


class BaseConfig:
    MONGO_URI: str = os.getenv("MONGO_URI")


class DevelopmentConfig(BaseConfig):
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    FASTAPI_ENV = os.getenv("FASTAPI_ENV", "development")


class ProductionConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    MONGO_URI = os.getenv(
        "TEST_MONGO_URI", "mongodb://localhost:27017/")
    FASTAPI_ENV = "testing"


@lru_cache()
def get_settings():
    config_cls_dict = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig
    }

    config_name = os.environ.get("FASTAPI_ENV", "development")
    config_cls = config_cls_dict[config_name]
    return config_cls()


settings = get_settings()
