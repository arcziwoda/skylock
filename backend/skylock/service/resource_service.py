import pathlib
from typing import List

from skylock.database import models as db_models
from skylock.database.repository import FileRepository, FolderRepository
from skylock.utils.exceptions import (
    InvalidPathException,
    ResourceAlreadyExistsException,
    ResourceNotFoundException,
)


class ResourceService:
    def __init__(
        self, file_repository: FileRepository, folder_repository: FolderRepository
    ):
        self._file_repository = file_repository
        self._folder_repository = folder_repository

    def get_folder_by_path(self, path: str) -> db_models.FolderEntity:
        parsed_path = self._parse_path(path)

        root_folder_name = parsed_path.parts[0]

        current_folder = self._get_root_folder_by_name(root_folder_name)

        for folder_name in parsed_path.relative_to(root_folder_name).parts:
            current_folder = self._folder_repository.get_by_name_and_parent_id(
                folder_name, current_folder.id
            )
            if current_folder is None:
                raise ResourceNotFoundException(missing_resource_name=folder_name)

        return current_folder

    def create_folder_for_user(self, path: str, user_id: str):
        parsed_path = self._parse_path(path)
        folder_name = parsed_path.name
        parent_path = parsed_path.parent
        parent = self.get_folder_by_path(str(parent_path))

        self._assert_no_children_matching_name(parent, folder_name)

        new_folder = db_models.FolderEntity(
            name=folder_name, parent_folder=parent, owner_id=user_id
        )
        new_folder = self._folder_repository.save(new_folder)

    def create_root_folder_for_user(self, user_id: str):
        folder_name = user_id
        self._folder_repository.save(
            db_models.FolderEntity(name=folder_name, owner_id=user_id)
        )

    def get_folder_children(
        self, folder: db_models.FolderEntity
    ) -> List[db_models.FolderEntity | db_models.FileEntity]:
        children = []
        children += folder.subfolders
        children += folder.files
        return children

    def _parse_path(self, path: str) -> pathlib.PurePosixPath:
        parsed_path = pathlib.PurePosixPath(path)

        if parsed_path.is_absolute():
            parsed_path = parsed_path.relative_to("/")

        if not parsed_path.parts:
            raise InvalidPathException

        return parsed_path

    def _get_root_folder_by_name(self, name: str) -> db_models.FolderEntity:
        folder = self._folder_repository.get_by_name_and_parent_id(name, None)
        if folder:
            return folder

        raise LookupError(f"This root folder doesn't exist: {name}")

    def _assert_no_children_matching_name(
        self, folder: db_models.FolderEntity, name: str
    ):
        children_names = [
            children.name for children in self.get_folder_children(folder)
        ]
        if name in children_names:
            raise ResourceAlreadyExistsException
