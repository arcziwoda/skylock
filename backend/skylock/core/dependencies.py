from skylock.repository.user_repository import UserRepository
from skylock.repository.config import SessionLocal
from skylock.service.user_service import UserService
from fastapi import Depends


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_repository(db=Depends(get_db)) -> UserRepository:
    return UserRepository(db)


def get_user_service(user_repository=Depends(get_user_repository)) -> UserService:
    return UserService(user_repository)
