from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"]

    DB_PATH: str

    @property
    def DATABASE_URL(self):
        return f"sqlite+aiosqlite:///{self.DB_PATH}"

    TEST_DB_PATH: str

    @property
    def TEST_DATABASE_URL(self):
        return f"sqlite+aiosqlite:///{self.TEST_DB_PATH}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
