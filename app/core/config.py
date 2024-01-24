from os import environ, path
from typing import List, Union

from dotenv import load_dotenv
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings

load_dotenv(verbose=True)


class Settings(BaseSettings):
    # ENV_STATE: str = environ.get("ENV_STATE", "dev")
    PROJECT_NAME: str = 'ab180-shorten-url'
    DOMAIN: str = environ.get("DOMAIN", "localhost")
    PORT: int = environ.get("PORT", "8080")
    BASE_DIR: str = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [f"http://{DOMAIN}", f"http://{DOMAIN}:{PORT}"]

    @field_validator("BACKEND_CORS_ORIGINS", mode='before')
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # sql
    MYSQL_SERVER: str = environ.get("MYSQL_SERVER", "localhost")
    MYSQL_USER: str = environ.get("MYSQL_USER", "admin")
    MYSQL_PASSWORD: str = environ.get("MYSQL_PASSWORD", "admin1234")
    MYSQL_DB: str = environ.get("MYSQL_DB", "test")
    DB_URL: str = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_SERVER}/{MYSQL_DB}"
    DB_POOL_SIZE: int = environ.get("DB_POOL_SIZE", 10)
    DB_POOL_MAX: int = environ.get("DB_POOL_MAX", 20)
    DB_POOL_RECYCLE: int = environ.get("DB_POOL_RECYCLE", 300)
    DB_POOL_TIMEOUT: int = environ.get("DB_POOL_TIMEOUT", 60)

    # redis
    REDIS_HOST: str = environ.get("REDIS_HOST", "localhost")
    REDIS_PORT: int = environ.get("REDIS_PORT", "6379")
    REDIS_PASSWORD: str = environ.get("REDIS_PASSWORD", "test1234")
    REDIS_URL: str = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}" \
        if REDIS_PASSWORD else f"redis://{REDIS_HOST}:{REDIS_PORT}"

    # mongo
    MONGO_DB_HOST: str = environ.get("MONGO_DB_HOST", "localhost")
    MONGO_DB_PORT: int = environ.get("MONGO_DB_PORT", 27017)
    MONGO_DB_USER: str = environ.get("MONGO_DB_USER", "admin")
    MONGO_DB_PASSWORD: str = environ.get("MONGO_DB_PASSWORD", "admin1234")
    MONGO_DB_URL: str = f"mongodb://{MONGO_DB_USER}:{MONGO_DB_PASSWORD}@{MONGO_DB_HOST}:{MONGO_DB_PORT}"
    MONGO_DB_NAME: str = environ.get("MONGO_DB_NAME", "short_click")

    class Config:
        case_sensitive = True


# class TestSettings(Settings):
#     MYSQL_DB: str = "test"
#     MONGO_DB_NAME: str = "test"
#
#
# class DevSettings(Settings):
#     MYSQL_DB: str = "dev"
#     MONGO_DB_NAME: str = "dev"
#
# @lru_cache
# def get_settings():
#     print(Settings().ENV_STATE)
#     env_state = Settings().ENV_STATE
#     if env_state == "test":
#         return TestSettings()
#     elif env_state == "dev":
#         return DevSettings()


settings = Settings()

