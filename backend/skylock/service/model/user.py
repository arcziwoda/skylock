from pydantic import BaseModel

from skylock.repository.model.user_entity import UserEntity


class User(BaseModel):
    id: int
    username: str

    @classmethod
    def from_entity(cls, entity: UserEntity):
        return cls(id=entity.id, username=entity.username)
