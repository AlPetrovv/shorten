from pathlib import Path

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent.parent.parent  # src
ROOT_DIR = BASE_DIR.parent  # app
ENV_FILE_DEV = ROOT_DIR / 'envs/dev/app.env'


class ApiV1(BaseModel):
    prefix: str = "/v1"


class Api(BaseModel):
    v1: ApiV1 = ApiV1()


class Database(BaseModel):
    """
    Database configuration model.

    This model is used to store the necessary database configuration
    for connecting to the database.
    """

    name: str = "database.db"  # change by env for test

    @property
    def url(self):
        return str(ROOT_DIR / self.name)


class Settings(BaseSettings):
    api: Api = Api()
    db: Database = Database()
    model_config = SettingsConfigDict(
        env_file=ENV_FILE_DEV,
        extra="allow",
        case_sensitive=False,
        env_prefix="APP_CONFIG__",
        env_nested_delimiter="__",
    )


settings = Settings()
