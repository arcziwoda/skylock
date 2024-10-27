import uuid

from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    username: str


class Token(BaseModel):
    access_token: str
    token_type: str


class LoginUserRequest(BaseModel):
    username: str
    password: str


class RegisterUserRequest(BaseModel):
    username: str
    password: str
