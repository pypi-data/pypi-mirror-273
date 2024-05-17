import toml
from pydantic_settings import BaseSettings

from .metadata import MetadataConfig


class __Settings(BaseSettings):
    metadata: MetadataConfig = MetadataConfig(**toml.load("pyproject.toml"))


Settings = __Settings()  # type: ignore[call-arg]
