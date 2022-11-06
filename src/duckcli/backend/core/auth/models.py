from sqlalchemy import Table, Column, MetaData
from sqlalchemy.sql.sqltypes import Boolean, Integer, String
from duckcli.backend.core.driver.database import sqlite_db

from duckcli.backend.core.settings.settings import get_core_settings


core_settings = get_core_settings()
# TODO add support for postgress DB etc
db_connection = sqlite_db(url=core_settings.db_url)

meta = MetaData()

Users = Table(
    "Users",
    meta,
    Column("id", Integer, unique=True, primary_key=True),
    Column("username", String),
    Column("email", String),
    Column("is_superuser", Boolean),
    Column("password", String),
)

meta.create_all(db_connection)
