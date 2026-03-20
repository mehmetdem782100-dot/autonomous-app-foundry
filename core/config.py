from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Cognita Core API"
    DATABASE_URL: str = "postgresql+asyncpg://cognita_user:cognita_password@localhost:5432/cognita_core_db"
    RABBITMQ_URL: str = "amqp://cognita_user:cognita_password@localhost:5672/"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
