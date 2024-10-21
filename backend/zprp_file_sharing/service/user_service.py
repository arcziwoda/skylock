import bcrypt
from ..repository.user_repository import UserRepository
from ..repository.model.user_entity import UserEntity
from ..core.security import create_jwt_for_user
from ..core.exceptions import UserAlreadyExists, InvalidCredentialsException


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def _hash_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def _verify_password(self, password: str, hashed_password: str):
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

    def register_user(self, username: str, password: str) -> str:
        existing_user = self.user_repository.get_user_by_username(username)
        if existing_user:
            raise UserAlreadyExists(f"User with username {username} already exists")

        hashed_password = self._hash_password(password)
        new_user = UserEntity(username=username, password=hashed_password)

        return self.user_repository.create_user(new_user)

    def verify_user(self, username: str, password: str) -> str:
        user = self.user_repository.get_user_by_username(username)
        if user and self._verify_password(password, str(user.password)):
            return create_jwt_for_user(username)
        raise InvalidCredentialsException
