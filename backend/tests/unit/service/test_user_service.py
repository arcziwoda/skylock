from unittest.mock import MagicMock, patch

import bcrypt
import pytest

from skylock.core.exceptions import (
    InvalidCredentialsException,
    UserAlreadyExists,
    UserNotFoundException,
)
from skylock.repository.model.user_entity import UserEntity
from skylock.repository.user_repository import UserRepository
from skylock.service.model.token import Token
from skylock.service.user_service import UserService


@pytest.fixture
def mock_user_repository():
    return MagicMock(spec=UserRepository)


@pytest.fixture
def user_service(mock_user_repository):
    return UserService(user_repository=mock_user_repository)


@pytest.fixture
def user_data():
    return {
        "id": 1,
        "username": "testuser",
        "password": "password123",
        "hashed_password": bcrypt.hashpw(
            "password123".encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8"),
    }


@pytest.fixture
def user_entity(user_data):
    return UserEntity(
        id=user_data["id"],
        username=user_data["username"],
        password=user_data["hashed_password"],
    )


def test_register_user_successful(
    user_service, mock_user_repository, user_data, user_entity
):
    mock_user_repository.get_user_by_username.return_value = None
    mock_user_repository.create_user.return_value = user_entity

    result = user_service.register_user(user_data["username"], user_data["password"])

    assert result.username == user_data["username"]
    mock_user_repository.get_user_by_username.assert_called_once_with(
        user_data["username"]
    )
    mock_user_repository.create_user.assert_called_once()


def test_register_user_already_exists(
    user_service, mock_user_repository, user_data, user_entity
):
    mock_user_repository.get_user_by_username.return_value = user_entity

    with pytest.raises(UserAlreadyExists):
        user_service.register_user(user_data["username"], user_data["password"])


def test_login_user_successful(
    user_service, mock_user_repository, user_data, user_entity
):
    mock_user_repository.get_user_by_username.return_value = user_entity

    with patch(
        "skylock.service.user_service.create_jwt_for_user",
        return_value="fake_jwt_token",
    ) as create_jwt_for_user_mock:
        result = user_service.login_user(user_data["username"], user_data["password"])

    assert isinstance(result, Token)
    assert result.access_token == "fake_jwt_token"
    assert result.token_type == "bearer"
    create_jwt_for_user_mock.assert_called_once_with(user_data["username"])
    mock_user_repository.get_user_by_username.assert_called_once_with(
        user_data["username"]
    )


def test_login_user_invalid_credentials(
    user_service, mock_user_repository, user_data, user_entity
):
    mock_user_repository.get_user_by_username.return_value = user_entity

    with pytest.raises(InvalidCredentialsException):
        user_service.login_user(user_data["username"], "wrong_password")


def test_login_user_not_found(user_service, mock_user_repository, user_data):
    mock_user_repository.get_user_by_username.return_value = None

    with pytest.raises(InvalidCredentialsException):
        user_service.login_user(user_data["username"], user_data["password"])


def test_get_user_by_username_successful(
    user_service, mock_user_repository, user_data, user_entity
):
    mock_user_repository.get_user_by_username.return_value = user_entity

    result = user_service.get_user_by_username(user_data["username"])

    assert result.username == user_data["username"]
    mock_user_repository.get_user_by_username.assert_called_once_with(
        user_data["username"]
    )


def test_get_user_by_username_not_found(user_service, mock_user_repository, user_data):
    mock_user_repository.get_user_by_username.return_value = None

    with pytest.raises(UserNotFoundException):
        user_service.get_user_by_username(user_data["username"])
