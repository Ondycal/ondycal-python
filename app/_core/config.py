from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    pg_dsn: PostgresDsn = "postgresql://postgres:secret@db/ondycal"


settings = Settings()
