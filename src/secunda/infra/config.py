from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ProjectBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        case_sensitive=False,
        extra="ignore",
        populate_by_name=True,
        protected_namespaces=(),
    )


class PostgresSettings(ProjectBaseSettings):
    host: str = Field(default="localhost")
    port: int = Field(default=5432)
    user: str = Field(default="postgres")
    password: str = Field(default="postgres")
    database: str = Field(default="secunda")

    model_config = SettingsConfigDict(env_prefix="POSTGRES_")

    def async_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}?ssl=disable"


class AppSettings(ProjectBaseSettings):
    debug: bool = Field(default=False)

    model_config = SettingsConfigDict(env_prefix="APP_")
