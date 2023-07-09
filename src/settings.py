from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class DbConfig(BaseModel):
    user: str
    password: str
    host: str
    port: int
    name: Optional[str] = ""


class Settings(BaseSettings):
    redis: DbConfig
    elastic_search: DbConfig

    class Config:
        env_file = "/code/.env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"
