from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    elasticsearch_url: str = "http://localhost:9200"
    rabbitmq_host: str = "localhost"

    model_config = SettingsConfigDict(
        env_file=".env")



settings = Settings()