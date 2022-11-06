from pydantic import BaseSettings, Field
from functools import lru_cache
import os

BASE_DIR = os.getcwd()


class Settings(BaseSettings):
    base_dir: str = os.getcwd()
    backend_username: str = Field("admin")
    backend_password: str = Field("Password123!")
    backend_token_url: str = Field("https://localhost:9999/auth/login")
    backend_inventory_url: str = Field("https://localhost:9999/inventory/device")
    backend_status_check_url: str = Field("https://localhost:9999/server/status")
    backend_ping_check_url: str = Field("https://localhost:9999/ping/start")
    backend_network_read_url: str = Field("https://localhost:9999/network/read/genie")

    verify_ssl_cert: bool = False

    class Config:
        env_prefix = "duckcli_"
        case_sensitive = False
        # env_nested_delimiter = '__'


settings = Settings()


@lru_cache()
def get_settings():
    return Settings()
