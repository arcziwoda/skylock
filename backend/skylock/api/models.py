from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class Folder(BaseModel):
    id: str
    name: str
    path: str
    is_public: bool


class File(BaseModel):
    id: str
    name: str
    path: str
    is_public: bool


class FolderContents(BaseModel):
    folder_name: str
    folder_path: str
    files: list[File]
    folders: list[Folder]


class LoginUserRequest(BaseModel):
    username: str
    password: str


class RegisterUserRequest(BaseModel):
    username: str
    password: str


class VisabilityRequest(BaseModel):
    is_public: bool


class UploadOptions(BaseModel):
    force: bool
    public: bool


class ResourceLocationResponse(BaseModel):
    location: str
