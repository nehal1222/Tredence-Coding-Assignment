from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./workflow_engine.db"
    LOG_LEVEL: str = "INFO"
    MAX_CONCURRENT_EXECUTIONS: int = 10
    
    class Config:
        env_file = ".env"

settings = Settings()
