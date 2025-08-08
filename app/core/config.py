from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int = 60
    database_url: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()