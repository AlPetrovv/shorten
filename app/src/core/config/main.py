from pathlib import Path

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent.parent.parent  # src
ROOT_DIR = BASE_DIR.parent  # app
ENV_FILE_DEV = ROOT_DIR.parent / 'envs/dev/local/app.env'


class Database(BaseModel):
    """
    Database configuration model.

    This model is used to store the necessary database configuration
    for connecting to the database.
    """

    url: str


class Settings(BaseSettings):
    db: Database = Field(description="DBSettings")
    model_config = SettingsConfigDict(
        env_file=ENV_FILE_DEV,
        extra="allow",
        case_sensitive=False,
        env_prefix="APP_CONFIG__",
        env_nested_delimiter="__",
    )


settings = Settings()  # noqa
