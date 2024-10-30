import uuid
from typing import Optional, List
from sqlalchemy import orm, ForeignKey


class Base(orm.DeclarativeBase):
    id: orm.Mapped[str] = orm.mapped_column(
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )


metadata = Base.metadata


class UserEntity(Base):
    __tablename__ = "users"

    username: orm.Mapped[str] = orm.mapped_column(unique=True, nullable=False)
    password: orm.Mapped[str] = orm.mapped_column(nullable=False)

    folders: orm.Mapped[List["FolderEntity"]] = orm.relationship(
        "FolderEntity", back_populates="owner", lazy="dynamic"
    )
    files: orm.Mapped[List["FileEntity"]] = orm.relationship(
        "FileEntity", back_populates="owner"
    )


class FolderEntity(Base):
    __tablename__ = "folders"

    name: orm.Mapped[str] = orm.mapped_column(nullable=False)
    parent_folder_id: orm.Mapped[Optional[int]] = orm.mapped_column(
        ForeignKey("folders.id")
    )
    owner_id: orm.Mapped[int] = orm.mapped_column(ForeignKey("users.id"))

    parent_folder: orm.Mapped[Optional["FolderEntity"]] = orm.relationship(
        "FolderEntity", remote_side="FolderEntity.id", back_populates="subfolders"
    )

    files: orm.Mapped[List["FileEntity"]] = orm.relationship(
        "FileEntity", back_populates="folder", lazy="dynamic"
    )

    subfolders: orm.Mapped[List["FolderEntity"]] = orm.relationship(
        "FolderEntity", back_populates="parent_folder", lazy="dynamic"
    )

    owner: orm.Mapped[UserEntity] = orm.relationship(
        "UserEntity", back_populates="folders"
    )


class FileEntity(Base):
    __tablename__ = "files"

    name: orm.Mapped[str] = orm.mapped_column(nullable=False)
    folder_id: orm.Mapped[int] = orm.mapped_column(ForeignKey("folders.id"))
    owner_id: orm.Mapped[int] = orm.mapped_column(ForeignKey("users.id"))
    disk_filepath: orm.Mapped[str] = orm.mapped_column(nullable=False)

    folder: orm.Mapped[FolderEntity] = orm.relationship(
        "FolderEntity", back_populates="files"
    )

    owner: orm.Mapped[UserEntity] = orm.relationship(
        "UserEntity", back_populates="files"
    )
