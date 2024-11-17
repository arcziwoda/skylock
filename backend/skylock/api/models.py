from pydantic import BaseModel


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
    files: list[File]
    folders: list[Folder]


class LoginUserRequest(BaseModel):
    username: str
    password: str


class RegisterUserRequest(BaseModel):
    username: str
    password: str
