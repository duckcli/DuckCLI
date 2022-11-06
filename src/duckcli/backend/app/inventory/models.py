from sqlalchemy import Table, Column, MetaData
from sqlalchemy.sql.sqltypes import Integer, String
from duckcli.backend.core.driver.database import sqlite_db
from duckcli.backend.core.settings.settings import get_core_settings


core_settings = get_core_settings()
db_connection = sqlite_db(url=core_settings.db_url)

meta = MetaData()

Devices = Table(
    "Inventory",
    meta,
    Column("id", Integer, unique=True, primary_key=True),
    Column("hostname", String),
    Column("vendor", String),
    Column("model", String),
    Column("osType", String),
    Column("mgmtIp", String),
    Column("driverType", String),
    Column("siteId", String),
    Column("region", String),
    Column("countryCode", String),
    Column("consoleServer", String),
    Column("consolePort", String),
    Column("softwareVersion", String),
    Column("automationEnabled", String),
    Column("deviceFunction", String),
    Column("deviceGroup", String),
    Column("operatingEnv", String),
    Column("itsmStrictMode", String),
    Column("changeControl", String),
)

meta.create_all(db_connection)
