import sqlalchemy as _sql
import sqlalchemy.orm as _orm

from duckcli.backend.core.settings.settings import get_core_settings

core_settings = get_core_settings()

# TODO: turn this into a factory class


def sqlite_db(url):
    engine = _sql.create_engine(url, connect_args={"check_same_thread": False})
    _ = _orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return engine.connect()


def db_session(url):
    if core_settings.db_type == "sqlite":
        return _extracted_from_db_session_5(url)
    if core_settings.db_type == "postgresql":
        return _extracted_from_db_session_5(url)


# TODO Rename this here and in `db_session`
def _extracted_from_db_session_5(url):
    # "sqlite:///SQLite.db"
    # db_url = f"{core_settings.db_type}:///{core_settings.db_name}.db"
    engine = _sql.create_engine(url)
    _ = _orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return engine.connect()
