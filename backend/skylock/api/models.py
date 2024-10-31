from typing import List

from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    username: str


class Token(BaseModel):
    access_token: str
    token_type: str


class Folder(BaseModel):
    name: str
    path: str


class File(BaseModel):
    name: str
    path: str


class FolderContents(BaseModel):
    files: List[File]
    folders: List[Folder]


class LoginUserRequest(BaseModel):
    username: str
    password: str


class RegisterUserRequest(BaseModel):
    username: str
    password: str
