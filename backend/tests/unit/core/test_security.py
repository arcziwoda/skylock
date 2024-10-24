from datetime import datetime, timedelta, timezone
from unittest.mock import patch
import pytest
from fastapi import HTTPException
from jose import jwt

from skylock.core.security import get_current_user

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
FAKE_JWT_SECRET = "fake_secret_for_testing"


@pytest.fixture
def username():
    return "testuser"


@pytest.fixture
def valid_token(username):
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": username, "exp": expire}
    return jwt.encode(to_encode, FAKE_JWT_SECRET, algorithm=ALGORITHM)


@pytest.fixture
def expired_token(username):
    expire = datetime.now(timezone.utc) - timedelta(minutes=1)
    to_encode = {"sub": username, "exp": expire}
    return jwt.encode(to_encode, FAKE_JWT_SECRET, algorithm=ALGORITHM)


@pytest.fixture
def invalid_token():
    return "invalid_token"


def test_get_current_user_valid_token(valid_token, username):
    with patch("skylock.core.security.JWT_SECRET", FAKE_JWT_SECRET):
        result = get_current_user(token=valid_token)

    assert result == username


def test_get_current_user_invalid_token(invalid_token):
    with patch("skylock.core.security.JWT_SECRET", FAKE_JWT_SECRET):
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(token=invalid_token)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid token"


def test_get_current_user_expired_token(expired_token):
    with patch("skylock.core.env.JWT_SECRET", FAKE_JWT_SECRET):
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(token=expired_token)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid token"
