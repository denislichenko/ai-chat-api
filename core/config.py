from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    OPENROUTER_API_KEY: str
    MODEL_NAME: str = "stepfun/step-3.5-flash:free"
    TEMPERATURE: float = 0.7

    class Config:
        env_file = ".env"

settings = Settings()