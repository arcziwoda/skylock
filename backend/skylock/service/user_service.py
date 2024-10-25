import bcrypt

from skylock.service.model.token import Token
from skylock.service.model.user import User
from skylock.repository.user_repository import UserRepository
from skylock.repository.model.user_entity import UserEntity
from skylock.core.security import create_jwt_for_user
from skylock.core.exceptions import (
    UserAlreadyExists,
    InvalidCredentialsException,
    UserNotFoundException,
)


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register_user(self, username: str, password: str) -> User:
        existing_user_entity = self.user_repository.get_user_by_username(username)
        if existing_user_entity:
            raise UserAlreadyExists(f"User with username {username} already exists")

        hashed_password = self._hash_password(password)
        new_user_entity = UserEntity(username=username, password=hashed_password)

        new_user_entity = self.user_repository.create_user(new_user_entity)

        return User.from_entity(new_user_entity)

    def login_user(self, username: str, password: str) -> Token:
        user_entity = self.user_repository.get_user_by_username(username)
        if user_entity and self._verify_password(password, user_entity.password):
            token = create_jwt_for_user(User.from_entity(user_entity))
            return Token(access_token=token, token_type="bearer")
        raise InvalidCredentialsException

    def get_user_by_username(self, username: str) -> User:
        user_entity = self.user_repository.get_user_by_username(username)
        if not user_entity:
            raise UserNotFoundException
        return User(id=user_entity.id, username=user_entity.username)

    def _hash_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def _verify_password(self, password: str, hashed_password: str):
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
