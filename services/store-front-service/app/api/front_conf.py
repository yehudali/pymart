from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    CATALOG_SERVICE_URL:str # = os.getenv("CATALOG_SERVICE_URL"),
    # user_management_url:str

    model_config = SettingsConfigDict(
        env_file=".env"
    )
    # ...עוד לפי כל סרוויס