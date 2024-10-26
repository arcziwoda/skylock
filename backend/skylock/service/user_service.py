import bcrypt

from skylock.api import models
from skylock.database.repository import UserRepository
from skylock.database import models as db_models
from skylock.utils.security import create_jwt_for_user
from skylock.utils.exceptions import (
    UserAlreadyExists,
    InvalidCredentialsException,
    UserNotFoundException,
)


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register_user(self, username: str, password: str) -> models.User:
        existing_user_entity = self.user_repository.get_by_username(username)
        if existing_user_entity:
            raise UserAlreadyExists(f"User with username {username} already exists")

        hashed_password = self._hash_password(password)
        new_user_entity = db_models.UserEntity(
            username=username, password=hashed_password
        )

        new_user_entity = self.user_repository.save(new_user_entity)

        return models.User.model_validate(new_user_entity)

    def login_user(self, username: str, password: str) -> models.Token:
        user_entity = self.user_repository.get_by_username(username)
        if user_entity and self._verify_password(password, user_entity.password):
            token = create_jwt_for_user(models.User.model_validate(user_entity))
            return models.Token(access_token=token, token_type="bearer")
        raise InvalidCredentialsException

    def get_by_username(self, username: str) -> models.User:
        user_entity = self.user_repository.get_by_username(username)
        if not user_entity:
            raise UserNotFoundException
        return models.User(id=user_entity.id, username=user_entity.username)

    def _hash_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def _verify_password(self, password: str, hashed_password: str):
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
