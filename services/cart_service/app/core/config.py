from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SECRET_KEY: str = "mysecretkey"
    CATALOG_SERVICE_URL: str = "http://catalog_management:8000"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
