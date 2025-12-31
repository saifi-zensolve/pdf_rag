import os
from datetime import UTC, datetime, timedelta

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()

    expire = datetime.now(UTC) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

    to_encode.update({"exp": expire})
    to_encode.update({"role": ["user"]})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        if "sub" not in payload:
            raise ValueError("The token is invalid or has expired")

        if "role" not in payload:
            raise ValueError("The token is invalid or has expired")

        if role := payload.get("role"):
            if not isinstance(role, list):
                raise ValueError("The token is invalid or has expired")

            return role.index("user") >= 0

        return False
    except JWTError as err:
        raise ValueError("The token is invalid or has expired") from err
    except Exception as err:
        raise ValueError("An error occurred while verifying the token") from err


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        if "username" not in payload:
            raise ValueError("The token is invalid or has expired")

        if "role" not in payload:
            raise ValueError("The token is invalid or has expired")

        return payload.get("username")
    except JWTError as err:
        raise ValueError("The token is invalid or has expired") from err
    except Exception as err:
        raise ValueError("An error occurred while verifying the token") from err
