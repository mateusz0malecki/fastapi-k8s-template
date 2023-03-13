from functools import lru_cache
from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    admin_email: str
    admin_password: str

    db_postgres_user: str
    db_postgres_name: str
    db_postgres_password: str
    db_postgres_host: str
    db_postgres_port: str
    db_postgres_url: PostgresDsn

    test_db_name: str
    test_db_url: PostgresDsn

    jwt_secret: str
    algorithm: str
    access_token_expire_minutes: int

    root_path: str

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


@lru_cache
def get_settings():
    return Settings()
