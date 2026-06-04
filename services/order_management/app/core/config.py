from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    
    SECRET_KEY:str = "mysecretkey"


    RABBITMQ_DEFAULT_USER: str = "yehuda"
    RABBITMQ_DEFAULT_PASS: str = "1234"

    RABBITMQ_HOST: str = "rabbitmq"
    RABBITMQ_PORT: int = 5672

    ELASTICSEARCH_URL: str = "http://elasticsearch:9200"
    USER_MANAGEMENT_URL: str = "http://user-service:8001"
    CART_SERVICE_URL:str = "http://cart-service:8003"
    

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
