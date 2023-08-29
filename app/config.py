from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    # Database Environment Variables
    DATABASE_HOSTNAME: str
    DB_PASSWORD: str
    DATABASE_PORT: str
    DATABASE_NAME: str
    DB_USERNAME: str

    # Authorization Environment Variables 
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # import values from .env file
    # never import in git (add .env file to gitignore)
    class Config:
        env_file = ".env"



Settings = Settings()