from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="env/.env", env_ignore_empty=True, extra="ignore"
    )
    TOKEN: str
    DATABSE_URL: str
    BOT_USERNAME: str
    CHAT_ID: str
    POOL_SIZE: int
    TIMEOUT: int
    RATE_LIMIT_REQUESTS: int
    RATE_LIMIT_PERIOD: int


settings = Settings()
