from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "BMI Calculator API"
    api_v1_prefix: str = "/api/v1"
    database_url: str = "sqlite:///./bmi_calculator.db"
    secret_key: str = "CHANGE_THIS_TO_A_LONG_RANDOM_SECRET"
    access_token_expire_minutes: int = 60 * 24
    algorithm: str = "HS256"
    cors_origins: str = "http://localhost:3000,http://localhost:8080,http://127.0.0.1:5500"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def allowed_origins(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
