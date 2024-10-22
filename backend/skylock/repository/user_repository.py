from sqlalchemy.orm import Session
from skylock.repository.model.user_entity import UserEntity


class UserRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_user_by_username(self, username: str) -> UserEntity:
        return (
            self.db_session.query(UserEntity)
            .filter(UserEntity.username == username)
            .first()
        )

    def create_user(self, user: UserEntity) -> UserEntity:
        self.db_session.add(user)
        self.db_session.commit()
        self.db_session.refresh(user)
        return user
