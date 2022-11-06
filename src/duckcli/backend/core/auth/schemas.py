import re
from pydantic import BaseModel, validator, validate_email
from typing import Optional


password_pattern = r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"

username_min_len_pattern = r"^[A-Za-z0-9].{4,}$"


class User(BaseModel):
    username: str
    email: str
    is_superuser: bool = False
    password: str

    @validator("username")
    def username_alphanumeric(cls, v):
        assert v.isalnum(), "must be a alphanumeric value"
        assert re.match(
            username_min_len_pattern, v
        ), "Username must be min 5 chars long"
        return v

    @validator("email")
    def email_address(cls, v):
        assert validate_email(v), "must be a valid email address"
        return v

    @validator("password")
    def valid_password(cls, v):
        assert re.match(
            password_pattern, v
        ), "must be a valid password - example: Dfr$rtg2"
        return v


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    is_superuser: Optional[bool] = None
