from typing import IO

from skylock.service.resource_service import ResourceService
from skylock.service.user_service import UserService
from skylock.api import models
from skylock.utils.exceptions import ForbiddenActionException
from skylock.utils.path import UserPath


class SkylockFacade:
    def __init__(self, user_service: UserService, resource_service: ResourceService):
        self._user_service = user_service
        self._resource_service = resource_service

    def register_user(self, username: str, password: str):
        user = self._user_service.register_user(username, password)
        self._resource_service.create_root_folder(UserPath.root_folder_of(user))

    def login_user(self, username: str, password: str) -> models.Token:
        return self._user_service.login_user(username, password)

    def create_folder_for_user(self, user_path: UserPath):
        self._resource_service.create_folder(user_path)

    def get_folder_contents(self, user_path: UserPath) -> models.FolderContents:
        folder = self._resource_service.get_folder(user_path)
        parent_path = f"/{user_path.path}" if user_path.path else ""
        children_files = [
            models.File(name=file.name, path=f"{parent_path}/{file.name}")
            for file in folder.files
        ]
        children_folders = [
            models.Folder(name=folder.name, path=f"{parent_path}/{folder.name}")
            for folder in folder.subfolders
        ]
        return models.FolderContents(files=children_files, folders=children_folders)

    def delete_folder(self, user_path: UserPath, is_recursively: bool = False):
        if user_path.is_root_folder():
            raise ForbiddenActionException("Deletion of root folder is forbidden")
        self._resource_service.delete_folder(user_path, is_recursively=is_recursively)

    def upload_file(self, user_path: UserPath, file_data: IO[bytes]):
        self._resource_service.create_file(user_path, file_data)

    def download_file(self, user_path: UserPath) -> IO[bytes]:
        return self._resource_service.get_file_data(user_path)
