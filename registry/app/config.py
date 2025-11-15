from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:postgres@localhost:5432/funcexec"
    jwt_secret_key: str = "your-secret-key-here-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 30

    # Resource limits
    max_memory_mb: int = 200
    max_cpu_cores: int = 1
    default_timeout_seconds: int = 30
    max_timeout_seconds: int = 60

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
