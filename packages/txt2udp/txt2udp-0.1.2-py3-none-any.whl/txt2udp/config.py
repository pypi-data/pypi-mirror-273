from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from enum import Enum


def parse_args(args_str: str) -> dict[str, str]:
    args = {}
    for arg in args_str.split(","):
        arg = arg.strip()
        if not arg:
            continue
        key, value = arg.split("=")
        args[key] = value
    return args


class TXT2UDPMode(str, Enum):
    server = "server"
    client = "client"


class Config(BaseSettings):

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    mode: TXT2UDPMode = Field(TXT2UDPMode.server, alias="TXT2UDP_MODE")
    host: str = Field("127.0.0.1", alias="TXT2UDP_HOST")
    port: int = Field(5000, alias="TXT2UDP_PORT")
    plugin: str = Field("stdio", alias="TXT2UDP_PLUGIN")
    plugin_args_str: str = Field("", alias="TXT2UDP_PLUGIN_ARGS")
    log_dir: str = Field("logs", alias="TXT2UDP_LOG_DIR")
    log_level: str = Field("DEBUG", alias="TXT2UDP_LOG_LEVEL")

    def get_plugin_args(self) -> dict[str, str]:
        return parse_args(self.plugin_args_str)


config = Config()
