from pydantic_settings import BaseSettings,SettingsConfigDict
from pathlib import Path 

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    app_name: str = "Test Technique FS"
    app_version: str = "1.0.0"
    debug: bool = True
    database_url: str 
    secret_key: str

    model_config = SettingsConfigDict(
        env_file=BASE_DIR/".env",
        case_sensitive=False,
    ) 


settings = Settings()