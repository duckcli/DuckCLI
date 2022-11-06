from pydantic import BaseSettings
from functools import lru_cache
import os
import sys
from enum import Enum

BASE_DIR = os.getcwd()
# print(BASE_DIR)
sys.path.append(f"{BASE_DIR}")


class DbTypeEnum(str, Enum):
    SQLite = "sqlite"
    PostgreSQL = "postgresql"


class Settings(BaseSettings):
    base_dir: str = os.getcwd()
    # Inventory settings
    inventory_type: str = "local_db"
    inventory_file: str = (
        f"{BASE_DIR}/src/duckcli/backend/core/inventory/inventroy_file.yaml"
    )
    inventory_fetch_limit: int = 500
    # JWT settings -  64 chrs (256bits) Must be set as ENV var
    jwt_secret_key: str = None
    jwt_access_token_expire_minutes: int = 600
    jwt_algorithm: str = "HS256"
    # DB settings
    db_type: DbTypeEnum = DbTypeEnum.SQLite
    # TODO: create url using validator logic
    db_url: str = "sqlite:///SQLite.db"
    db_hostname: str = None  # IP address or hostname
    db_port: int = None
    db_name: str = "SQLite"
    db_username: str = None
    db_password: str = None
    # SSL
    verify_ssl_cert: bool = False
    # Regex patterns
    password_pattern: str = (
        r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
    )

    username_min_len_pattern: str = r"^[A-Za-z0-9].{4,}$"

    class Config:
        env_prefix = "duckcli_"
        case_sensitive = False
        # env_nested_delimiter = '__'


settings = Settings()


@lru_cache()
def get_core_settings():
    return Settings()
