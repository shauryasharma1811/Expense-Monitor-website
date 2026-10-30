from pydantic_settings import BaseSettings
from pydantic import model_validator

class Settings(BaseSettings):
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DATABASE_URL: str = "sqlite:///./test.db"
    SECRET_KEY: str = "test-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ENCRYPTION_KEY: str = "test-encryption-key-32-bytes-long-string=="
    GOOGLE_CLIENT_ID: str = "placeholder-google-client-id.apps.googleusercontent.com"
    GOOGLE_CLIENT_SECRET: str = "placeholder-google-client-secret"

    @model_validator(mode="after")
    def validate_production_secrets(self) -> "Settings":
        if self.ENVIRONMENT.lower() == "production":
            if not self.SECRET_KEY or self.SECRET_KEY in ("test-secret-key", "dev-secret-do-not-use-in-prod"):
                raise ValueError("PRODUCTION ERROR: SECRET_KEY must be set to a secure secret in production!")
            if not self.ENCRYPTION_KEY or self.ENCRYPTION_KEY == "test-encryption-key-32-bytes-long-string==":
                raise ValueError("PRODUCTION ERROR: ENCRYPTION_KEY must be set to a secure Fernet key in production!")
        return self

    class Config:
        env_file = ".env"
        extra = "ignore"
