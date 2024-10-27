import uuid

from sqlalchemy import orm


class Base(orm.DeclarativeBase):
    id: orm.Mapped[uuid.UUID] = orm.mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )


metadata = Base.metadata


class UserEntity(Base):
    __tablename__ = "users"

    username: orm.Mapped[str] = orm.mapped_column(unique=True, nullable=False)
    password: orm.Mapped[str] = orm.mapped_column(nullable=False)
