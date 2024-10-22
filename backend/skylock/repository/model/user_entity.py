from sqlalchemy import String, Integer
from sqlalchemy.orm import mapped_column
from skylock.repository.config import Base


class UserEntity(Base):
    __tablename__ = "users"

    id = mapped_column(Integer, primary_key=True, index=True)
    username = mapped_column(String, unique=True, nullable=False)
    password = mapped_column(String, nullable=False)
