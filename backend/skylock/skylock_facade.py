from skylock.service.resource_service import ResourceService
from skylock.service.user_service import UserService
from skylock.api import models
from skylock.utils.exceptions import ForbiddenActionException
from skylock.utils.path import SkylockPath


class SkylockFacade:
    def __init__(self, user_service: UserService, resource_service: ResourceService):
        self._user_service = user_service
        self._resource_service = resource_service

    def register_user(self, username: str, password: str):
        user = self._user_service.register_user(username, password)
        user_path = self._create_user_path(".", models.User.model_validate(user))
        self._resource_service.create_root_folder_for_user(user.id, user_path)

    def login_user(self, username: str, password: str) -> models.Token:
        return self._user_service.login_user(username, password)

    def create_folder_for_user(self, path: str, user: models.User):
        user_path = self._create_user_path(path, user)
        self._resource_service.create_folder_for_user(user_path, user.id)

    def get_folder_contents(
        self, path: str, user: models.User
    ) -> models.FolderContents:
        user_path = self._create_user_path(path, user)
        folder = self._resource_service.get_folder_by_path(user_path)
        children_files = [
            models.File(name=file.name, path=f"{path}/{file.name}")
            for file in folder.files
        ]
        children_folders = [
            models.Folder(name=folder.name, path=f"{path}/{folder.name}")
            for folder in folder.subfolders
        ]
        return models.FolderContents(files=children_files, folders=children_folders)

    def delete_folder(self, path: str, user: models.User, is_recursively: bool = False):
        user_path = self._create_user_path(path, user)
        if user_path.is_root_folder():
            raise ForbiddenActionException("Deletion of root folder is forbidden")
        self._resource_service.delete_folder(user_path, is_recursively=is_recursively)

    def _create_user_path(self, path: str, user: models.User) -> SkylockPath:
        return SkylockPath(path=path, root_folder_name=user.id)
