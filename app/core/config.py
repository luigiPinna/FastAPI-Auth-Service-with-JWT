from typing import List
from pydantic_settings import BaseSettings
from pydantic import computed_field


class Settings(BaseSettings):
    # Base
    PROJECT_NAME: str
    VERSION: str
    API_V1_STR: str
    DEBUG: bool

    # CORS - deve arrivare dal .env
    BACKEND_CORS_ORIGINS: str

    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Database
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        """URL database calcolato automaticamente"""
        return (
            f"postgresql://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_SERVER}/"
            f"{self.POSTGRES_DB}"
        )

    @computed_field
    @property
    def CORS_ORIGINS_LIST(self) -> List[str]:
        """Lista origins CORS pulita"""
        return [origin.strip() for origin in self.BACKEND_CORS_ORIGINS.split(",")]

    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_MINUTES: int = 1

    model_config = {
        "case_sensitive": True,
        "env_file": ".env",
        "extra": "forbid"
    }


settings = Settings()