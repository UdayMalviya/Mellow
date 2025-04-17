from functools import lru_cache
from pydantic import  Field, field_validator
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # === Application Environment ===
    environment: str = Field(default="test", alias="ENVIRONMENT")  # dev, prod, test

    # === Database Credentials ===
    database_type: str = Field(..., alias="DATABASE_TYPE")
    database_host: str = Field(..., alias="DATABASE_HOST")
    database_port: int = Field(..., alias="DATABASE_PORT")
    database_username: str = Field(..., alias="DATABASE_USERNAME")
    database_password: str = Field(..., alias="DATABASE_PASSWORD")
    database_name: str = Field(..., alias="DATABASE_NAME")
    # database_test_name: Optional[str] = Field(None, alias="DATABASE_TEST_NAME")  # Optional for non-test env

    # === JWT / Auth Settings ===
    jwt_secret_key: str = Field(..., alias="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(default=30, alias="ACCESS_TOKEN_EXPIRE_MINUTES")

    # === Redis / Optional Services (example) ===
    # redis_url: Optional[str] = Field(None, alias="REDIS_URL")

    # === Computed Database URL ===
    @property
    def database_url(self) -> str:
        # db_name = self.database_test_name if self.environment == "test" and self.database_test_name else self.database_name
        return (
            f"{self.database_type}+psycopg2://"
            f"{self.database_username}:{self.database_password}@"
            f"{self.database_host}:{self.database_port}/{self.database_name}"
        )

    # === Validators ===
    @field_validator('database_type', 'database_host', 'database_username', 'database_password', 'database_name')
    @classmethod
    def must_not_be_empty(cls, value: str, info):
        if not value.strip():
            raise ValueError(f"Environment variable '{info.field_name.upper()}' is required and cannot be empty")
        return value

    @field_validator('database_port')
    @classmethod
    def must_be_valid_port(cls, value: int):
        if not (1 <= value <= 65535):
            raise ValueError("DATABASE_PORT must be a valid port number (1-65535)")
        return value

    model_config = {
        "env_file": ".env",  # Optional fallback to .env file
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
        "populate_by_name": True  # Enables alias-to-field name mapping
    }


# Singleton Settings Instance
@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

print(settings.database_url)