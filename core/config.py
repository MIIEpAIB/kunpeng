from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Kunpeng Yidao API"
    debug: bool = True

    # JWT
    secret_key: str = "change-this-secret-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 8

    # Database
    mysql_user: str = "kunpeng"
    mysql_password: str = "HdPBDCX"
    mysql_host: str = "127.0.0.1"
    mysql_port: int = 3306
    mysql_db: str = "kunpeng"

    class Config:
        env_prefix = "KUNPENG_"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    return Settings()

