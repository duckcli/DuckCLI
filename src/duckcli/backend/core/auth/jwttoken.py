from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt

# app modules
from duckcli.backend.core.auth.schemas import TokenData
from duckcli.backend.core.settings.settings import get_core_settings

core_settings = get_core_settings()
# from main import TokenData

JWT_SECRET_KEY = core_settings.jwt_secret_key
ALGORITHM = core_settings.jwt_algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = core_settings.jwt_access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode["exp"] = expire
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
        is_superuser: bool = payload.get("is_superuser")
        email: str = payload.get("email")
        return TokenData(username=username, email=email, is_superuser=is_superuser)

    except JWTError as e:
        raise credentials_exception from e
