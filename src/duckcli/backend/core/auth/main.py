from fastapi import APIRouter, Depends
from duckcli.backend.core.driver.database import sqlite_db
from fastapi.security import OAuth2PasswordRequestForm
from duckcli.backend.core.auth.jwttoken import create_access_token
from duckcli.backend.core.auth.oauth import get_current_user
from duckcli.backend.core.auth.hashing import Hash
from duckcli.backend.core.auth.schemas import User
from duckcli.backend.core.auth.models import Users

from duckcli.backend.core.settings.settings import get_core_settings


core_settings = get_core_settings()
db_connection = sqlite_db(url=core_settings.db_url)

auth = APIRouter()


@auth.get("/verify_token")
def verify_token(current_user: User = Depends(get_current_user)):
    return current_user


@auth.get("/users")
def retrieve_all_user(user: User = Depends(verify_token)):
    if user.is_superuser:
        return db_connection.execute(Users.select()).fetchall()
    else:
        return [{"error": "Not enough permissions"}]


@auth.get("/user/{username}")
def retrieve_one_user(username: str, user: User = Depends(verify_token)):
    if username == user.username or user.is_superuser:
        return db_connection.execute(
            Users.select().where(Users.c.username == username)
        ).fetchall()
    else:
        return [{"error": "Not enough permissions"}]


@auth.patch("/user/{username}")
def update_user_data(username: str, req: User, user: User = Depends(verify_token)):
    if req.username != username:
        return [{"error": "Username in the path and the payload does not match"}]
    if req.username != user.username and not user.is_superuser:
        return [
            {
                "error": f"Not enough permission. User {user.username} is trying to update user {req.username} login details"
            }
        ]
    db_connection.execute(
        Users.update()
        .values(
            username=req.username,
            email=req.email,
            password=Hash.bcrypt(req.password),
        )
        .where(Users.c.username == username)
    )
    return db_connection.execute(
        Users.select().where(Users.c.username == username)
    ).fetchall()


@auth.delete("/user/{username}")
def delete_user_data(username: str, user: User = Depends(verify_token)):
    if not user.is_superuser:
        return [{"error": "Not enough permissions"}]
    exists = db_connection.execute(
        Users.select().where(Users.c.username == username)
    ).fetchall()
    if not exists:
        return [{"message": f"{username} user not found"}]
    db_connection.execute(Users.delete().where(Users.c.username == username))
    return [{"message": f"{username} user got deleted"}]


@auth.post("/register")
def create_user(req: User, user: User = Depends(verify_token)):
    if user.is_superuser:
        if db_connection.execute(
            Users.select().where(Users.c.username == req.username)
        ).fetchall():
            return db_connection.execute(
                Users.select().where(Users.c.username == req.username)
            ).fetchall()
        try:
            db_connection.execute(
                Users.insert().values(
                    username=req.username,
                    email=req.email,
                    is_superuser=req.is_superuser,
                    password=Hash.bcrypt(req.password),
                )
            )
            return db_connection.execute(
                Users.select().where(Users.c.username == req.username)
            ).fetchall()
        except Exception as error:
            print(error)


@auth.post("/login")
def login(req: OAuth2PasswordRequestForm = Depends()):
    user = db_connection.execute(
        Users.select().where(Users.c.username == req.username)
    ).fetchone()
    if not user:
        return {"error": f"No user found with this {req.username} username"}
    if not Hash.verify(user[-1], req.password):
        return {"error": "Wrong Username or password"}
    access_token = create_access_token(
        data={"username": user[1], "email": user[2], "is_superuser": user[3]}
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "id": user[0],
        "is_superuser": user[3],
    }


@auth.patch("/superuser/{username}/{enable}")
def change_superuser(username: str, enable: bool, user: User = Depends(verify_token)):
    if user.is_superuser:
        db_connection.execute(
            Users.update()
            .values(is_superuser=enable)
            .where(Users.c.username == username)
        )

        return db_connection.execute(
            Users.select().where(Users.c.username == username)
        ).fetchall()
    else:
        return [{"error": "Not enough permissions"}]
