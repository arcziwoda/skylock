from skylock.database import models as db_models
from skylock.database.repository import FileRepository, FolderRepository
from skylock.utils.exceptions import (
    FolderNotEmptyException,
    ForbiddenActionException,
    ResourceAlreadyExistsException,
    ResourceNotFoundException,
)
from skylock.utils.path import UserPath


class ResourceService:
    def __init__(
        self, file_repository: FileRepository, folder_repository: FolderRepository
    ):
        self._file_repository = file_repository
        self._folder_repository = folder_repository

    def get_folder(self, user_path: UserPath) -> db_models.FolderEntity:
        current_folder = self._get_root_folder_by_name(user_path.root_folder_name)

        for folder_name in user_path.parts:
            current_folder = self._folder_repository.get_by_name_and_parent_id(
                folder_name, current_folder.id
            )
            if current_folder is None:
                raise ResourceNotFoundException(missing_resource_name=folder_name)

        return current_folder

    def create_folder(self, user_path: UserPath):
        if user_path.is_root_folder():
            raise ForbiddenActionException("Creation of root folder is forbidden")

        folder_name = user_path.name
        parent_path = user_path.parent
        parent = self.get_folder(parent_path)

        self._assert_no_children_matching_name(parent, folder_name)

        new_folder = db_models.FolderEntity(
            name=folder_name, parent_folder=parent, owner=user_path.owner
        )
        new_folder = self._folder_repository.save(new_folder)

    def delete_folder(self, user_path: UserPath, is_recursively: bool = False):
        folder = self.get_folder(user_path)

        if folder.is_root():
            raise ForbiddenActionException("Deletion of root folder is forbidden")

        has_folder_children = bool(folder.subfolders or folder.files)
        if not is_recursively and has_folder_children:
            raise FolderNotEmptyException

        self._folder_repository.delete(folder)

    def create_root_folder(self, user_path: UserPath):
        self._folder_repository.save(
            db_models.FolderEntity(
                name=user_path.root_folder_name, owner=user_path.owner
            )
        )

    def _get_root_folder_by_name(self, name: str) -> db_models.FolderEntity:
        folder = self._folder_repository.get_by_name_and_parent_id(name, None)
        if folder:
            return folder

        raise LookupError(f"This root folder doesn't exist: {name}")

    def _assert_no_children_matching_name(
        self, folder: db_models.FolderEntity, name: str
    ):
        exists_file_of_name = name in [file.name for file in folder.files]
        exists_folder_of_name = name in [folder.name for folder in folder.subfolders]
        if exists_file_of_name or exists_folder_of_name:
            raise ResourceAlreadyExistsException
