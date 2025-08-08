from pydantic import BaseSettings


class Settings(BaseSettings):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int = 60
    database_url: str

    class Config:
        env_file = ".env"


settings = Settings()