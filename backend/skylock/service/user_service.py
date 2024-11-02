import argon2

from skylock.api import models
from skylock.database.repository import UserRepository
from skylock.database import models as db_models
from skylock.utils.security import create_jwt_for_user
from skylock.utils.exceptions import (
    UserAlreadyExists,
    InvalidCredentialsException,
)


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        self.password_hasher = argon2.PasswordHasher()

    def register_user(self, username: str, password: str) -> db_models.UserEntity:
        existing_user_entity = self.user_repository.get_by_username(username)
        if existing_user_entity:
            raise UserAlreadyExists(f"User with username {username} already exists")

        hashed_password = self.password_hasher.hash(password)
        new_user_entity = db_models.UserEntity(
            username=username, password=hashed_password
        )

        return self.user_repository.save(new_user_entity)

    def login_user(self, username: str, password: str) -> models.Token:
        user_entity = self.user_repository.get_by_username(username)
        if user_entity and self._verify_password(user_entity.password, password):
            token = create_jwt_for_user(user_entity)
            return models.Token(access_token=token, token_type="bearer")
        raise InvalidCredentialsException

    def verify_user(self, username: str, password: str) -> bool:
        user_entity = self.user_repository.get_by_username(username)
        if user_entity and self._verify_password(user_entity.password, password):
            return True
        return False

    def _verify_password(self, hashed_password, password) -> bool:
        try:
            self.password_hasher.verify(hashed_password, password)
            return True
        except argon2.exceptions.VerifyMismatchError:
            return False
