# Location: src/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """Application settings from environment variables."""
    
    app_name: str = "SupportGPT"
    app_version: str = "0.1.0"
    environment: str = "development"
    debug: bool = True
    
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
        # Database
    database_url: str = "postgresql+asyncpg://supportgpt:supportgpt_password@postgres:5432/supportgpt_db"
    database_echo: bool = True
    
    # Redis
    redis_url: str = "redis://redis:6379/0"
    redis_ttl: int = 3600  # 1 hour
    
    # Rate Limiting
    rate_limit_requests: int = 100
    rate_limit_period: int = 60  # seconds
    
    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()