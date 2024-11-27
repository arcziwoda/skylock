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

    def create_folder_for_user(self, user_path: UserPath) -> models.Folder:
        folder_entity = self._resource_service.create_folder(user_path)
        return models.Folder(
            name=folder_entity.name, path=user_path.parent.path, is_public=folder_entity.is_public
        )

    def get_folder_contents(self, user_path: UserPath) -> models.FolderContents:
        folder = self._resource_service.get_folder(user_path)
        parent_path = f"/{user_path.path}" if user_path.path else ""
        children_files = [
            models.File(name=file.name, is_public=file.is_public, path=f"{parent_path}/{file.name}")
            for file in folder.files
        ]
        children_folders = [
            models.Folder(
                name=folder.name, is_public=folder.is_public, path=f"{parent_path}/{folder.name}"
            )
            for folder in folder.subfolders
        ]
        return models.FolderContents(files=children_files, folders=children_folders)

    def get_public_folder_contents(self, folder_id: str) -> models.FolderContents:
        current_folder = self._resource_service.get_public_folder(folder_id)

        children_files = [
            models.File(
                name=file.name, is_public=file.is_public, path=f"{current_folder.name}/{file.name}"
            )
            for file in current_folder.files
        ]
        children_folders = [
            models.Folder(
                name=folder.name,
                is_public=folder.is_public,
                path=f"{current_folder.name}/{folder.name}",
            )
            for folder in current_folder.subfolders
        ]
        return models.FolderContents(files=children_files, folders=children_folders)

    def delete_folder(self, user_path: UserPath, is_recursively: bool = False):
        if user_path.is_root_folder():
            raise ForbiddenActionException("Deletion of root folder is forbidden")
        self._resource_service.delete_folder(user_path, is_recursively=is_recursively)

    def update_folder_visability(self, user_path: UserPath, is_public: bool):
        folder = self._resource_service.get_folder(user_path)
        folder.is_public = is_public
        self._resource_service.update_folder(folder)

    def update_file_visability(self, user_path: UserPath, is_public: bool):
        file = self._resource_service.get_file(user_path)
        file.is_public = is_public
        self._resource_service.update_file(file)

    def upload_file(self, user_path: UserPath, file_data: IO[bytes], force:bool, public:bool) -> models.File:
        file_entity = self._resource_service.create_file(user_path, file_data, force, public)
        return models.File(
            name=file_entity.name, path=user_path.parent.path, is_public=file_entity.is_public
        )

    def download_file(self, user_path: UserPath) -> IO[bytes]:
        return self._resource_service.get_file_data(user_path)

    def download_public_file(self, file_id: str) -> IO[bytes]:
        return self._resource_service.get_public_file_data(file_id)

    def delete_file(self, user_path: UserPath):
        self._resource_service.delete_file(user_path)
