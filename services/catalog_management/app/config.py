import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    
    SECRET_KEY: str = "mysecretkey"

    ELASTICSEARCH_URL:str
    
    MINIO_URL:str
    MINIO_ACCESS_KEY:str
    MINIO_SECRET_KEY:str


    model_config = SettingsConfigDict(env_file=".env")


settings = Settings() # type: ignore
