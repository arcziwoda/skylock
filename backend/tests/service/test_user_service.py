import pytest
from skylock.core.exceptions import (
    UserAlreadyExists,
    InvalidCredentialsException,
    UserNotFoundException,
)
from skylock.service.model.user import User
from ..conftest import user_service


@pytest.mark.usefixtures("user_service")
class TestUserService:

    def test_register_user_success(self, user_service):
        username = "testuser"
        password = "securepassword"

        user = user_service.register_user(username, password)

        assert user.username == username
        assert user.id is not None

    def test_register_user_already_exists(self, user_service):
        username = "existinguser"
        password = "securepassword"

        user_service.register_user(username, password)

        with pytest.raises(UserAlreadyExists):
            user_service.register_user(username, password)

    def test_login_user_success(self, user_service):
        username = "loginuser"
        password = "securepassword"

        user_service.register_user(username, password)

        token = user_service.login_user(username, password)

        assert token.access_token is not None
        assert token.token_type == "bearer"

    def test_login_user_invalid_credentials(self, user_service):
        username = "invaliduser"
        password = "wrongpassword"

        with pytest.raises(InvalidCredentialsException):
            user_service.login_user(username, password)

    def test_login_user_wrong_password(self, user_service):
        username = "anotheruser"
        password = "securepassword"

        user_service.register_user(username, password)

        with pytest.raises(InvalidCredentialsException):
            user_service.login_user(username, "wrongpassword")

    def test_get_user_by_username_success(self, user_service):
        username = "getuser"
        password = "securepassword"

        user_service.register_user(username, password)

        user: User = user_service.get_user_by_username(username)

        assert user.username == username
        assert user.id is not None

    def test_get_user_by_username_not_found(self, user_service):
        username = "nonexistentuser"

        with pytest.raises(UserNotFoundException):
            user_service.get_user_by_username(username)
