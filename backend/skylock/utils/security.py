from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from skylock.config import JWT_SECRET
from skylock.api import models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def get_current_user(
    token: str = Depends(oauth2_scheme),
) -> models.User:
    try:
        user = get_user_from_jwt(token)
    except JWTError as e:
        raise HTTPException(status_code=401, detail="Invalid token") from e

    if user is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    return user


def create_jwt_for_user(user: models.User) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"id": str(user.id), "sub": user.username, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)
    return encoded_jwt


def get_user_from_jwt(token: str) -> Optional[models.User]:
    payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
    user_id = payload.get("id")
    username = payload.get("sub")
    if user_id and username:
        return models.User(id=user_id, username=username)
    return None
