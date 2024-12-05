from skylock.database.repository import FileRepository, FolderRepository
from skylock.database import models as db_models
from skylock.utils.exceptions import ResourceNotFoundException
from skylock.utils.path import UserPath


class PathResolver:
    def __init__(self, file_repository: FileRepository, folder_repository: FolderRepository):
        self._file_repository = file_repository
        self._folder_repository = folder_repository

    def resolve_for_folder(self, user_path: UserPath) -> db_models.FolderEntity:
        current_folder = self._get_root_folder(user_path.root_folder_name)

        if current_folder is None:
            raise LookupError(f"Root folder: {user_path.root_folder_name} does not exist")

        for folder_name in user_path.parts:
            current_folder = self._folder_repository.get_by_name_and_parent_id(
                folder_name, current_folder.id
            )
            if current_folder is None:
                raise ResourceNotFoundException(missing_resource_name=folder_name)

        return current_folder

    def resolve_for_file(self, user_path: UserPath) -> db_models.FileEntity:
        parent_folder = self.resolve_for_folder(user_path.parent)
        file = self._file_repository.get_by_name_and_parent(
            name=user_path.name, parent=parent_folder
        )

        if file is None:
            raise ResourceNotFoundException(missing_resource_name=user_path.name)

        return file

    def _get_root_folder(self, name: str) -> db_models.FolderEntity | None:
        return self._folder_repository.get_by_name_and_parent_id(name=name, parent_id=None)
