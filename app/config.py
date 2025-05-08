"""App configuration file."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    """Database settings for the project.

    Attributes:
        NAME: Name of the database.
        HOST: Hostname of the database.
        USER: Username of the database.
        PASS: Password of the database.
        PORT: Port number of the database.
    """

    model_config = SettingsConfigDict(env_prefix="_")

    NAME: str
    HOST: str
    USER: str
    PASS: str
    PORT: int


class Settings(BaseSettings):
    """Settings for the project."""

    model_config = SettingsConfigDict(env_nested_delimiter="__")

    DB: DatabaseSettings
    JWT_SECRET: str
    LOG_LEVEL: str = "info"


settings: Settings = Settings()
