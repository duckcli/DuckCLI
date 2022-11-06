import re
import typer
from pydantic import validate_email
from duckcli.backend.core.settings.settings import get_core_settings
from duckcli.backend.core.auth.models import Users
from duckcli.backend.core.driver.database import sqlite_db
from duckcli.backend.core.auth.hashing import Hash


core_settings = get_core_settings()
db_connection = sqlite_db(url=core_settings.db_url)
username_min_len_pattern = core_settings.username_min_len_pattern
password_pattern = core_settings.password_pattern[0]

app = typer.Typer()


@app.command()
def create_user(username: str, password: str, email: str, is_superuser: bool = False):
    try:
        assert username.isalnum(), "must be a alphanumeric value"
        assert re.match(
            username_min_len_pattern, username
        ), "Username must be min 5 chars long"

        assert validate_email(email), "must be a valid email address"

        assert re.match(
            password_pattern, password
        ), "must be a valid password - example: <Upper-lower-&pecialChar-4umber-min-8>"

    except AssertionError as assertion_error:

        print(assertion_error)
        exit()

    if db_connection.execute(
        Users.select().where(Users.c.username == username)
    ).fetchall():
        print("Username already exist in the DB")
        return 0

    try:
        print(f"Creating new user {username}")
        db_connection.execute(
            Users.insert().values(
                username=username,
                email=email,
                is_superuser=is_superuser,
                password=Hash.bcrypt(password),
            )
        )

        user_info = db_connection.execute(
            Users.select().where(Users.c.username == username)
        ).fetchall()
        print(user_info)
        print("Done")
    except Exception as error:
        print(error)


@app.command()
def admin_other():
    raise NotImplementedError


def main():
    app()


if __name__ == "__main__":
    app()
