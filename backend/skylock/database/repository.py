import uuid
from typing import Generic, TypeVar, Type, Optional
from sqlalchemy import BinaryExpression, select
from sqlalchemy.orm import Session
from skylock.database import models

Model = TypeVar("Model", bound=models.Base)


class DatabaseRepository(Generic[Model]):
    def __init__(self, model: Type[Model], session: Session) -> None:
        self.model = model
        self.session = session

    def save(self, entity: Model) -> Model:
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def get_by_id(self, entity_id: uuid.UUID) -> Optional[Model]:
        return self.session.get(self.model, entity_id)

    def filter(self, *expressions: BinaryExpression) -> list[Model]:
        query = select(self.model)
        if expressions:
            query = query.where(*expressions)
        return list(self.session.execute(query).scalars().all())


class UserRepository(DatabaseRepository[models.UserEntity]):
    def __init__(self, session: Session):
        super().__init__(models.UserEntity, session)

    def get_by_username(self, username: str) -> Optional[models.UserEntity]:
        stmt = select(self.model).where(models.UserEntity.username == username)
        result = self.session.execute(stmt).scalar_one_or_none()
        return result


class FolderRepository(DatabaseRepository[models.FolderEntity]):
    def __init__(self, session: Session):
        super().__init__(models.FolderEntity, session)

    def get_by_name_and_parent_id(
        self, name: str, parent_id: uuid.UUID | None
    ) -> Optional[models.FolderEntity]:
        stmt = select(self.model).where(
            models.FolderEntity.name == name
            and models.FolderEntity.parent_folder_id == parent_id
        )
        result = self.session.execute(stmt).scalar_one_or_none()
        return result


class FileRepository(DatabaseRepository[models.FileEntity]):
    def __init__(self, session: Session):
        super().__init__(models.FileEntity, session)
