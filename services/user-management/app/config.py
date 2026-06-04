from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ELASTICSEARCH_HOST:str = "elasticsearch"
    ELASTICSEARCH_PORT:int = 9200
    SECRET_KEY:str = "mysecretkey"


    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
