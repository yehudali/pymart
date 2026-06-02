from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    elasticsearch_url: str = "http://localhost:9200"
  
    RABBITMQ_HOST:str = "rabbitmq"
    RABBITMQ_PORT:int = 5672

    RABBITMQ_DEFAULT_USER: str = "yehuda"
    RABBITMQ_DEFAULT_PASS: str = "1234"

    model_config = SettingsConfigDict(
        env_file=".env")



settings = Settings()