from fastapi import Depends

from skylock.database.repository import UserRepository
from skylock.database.session import get_db_session
from skylock.service.user_service import UserService


def get_user_repository(db=Depends(get_db_session)) -> UserRepository:
    return UserRepository(db)


def get_user_service(user_repository=Depends(get_user_repository)) -> UserService:
    return UserService(user_repository)
