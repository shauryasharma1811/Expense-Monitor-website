from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_VERSION: str = "1.0.0"
    DATABASE_URL: str = "sqlite:///./test.db"
    SECRET_KEY: str = "test-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ENCRYPTION_KEY: str = "test-encryption-key-32-bytes-long-string=="

    class Config:
        env_file = ".env"
        extra = "ignore"
