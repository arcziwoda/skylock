import pathlib
import uuid
from typing import List

from skylock.database import models as db_models
from skylock.database.repository import FileRepository, FolderRepository


class ResourceService:
    def __init__(
        self, file_repository: FileRepository, folder_repository: FolderRepository
    ):
        self._file_repository = file_repository
        self._folder_repository = folder_repository

    def get_folder_by_path(self, path: str) -> db_models.FolderEntity:
        print(path)
        parsed_path = self._parse_path(path)

        root_folder_name = parsed_path.parts[0]

        current_folder = self._get_root_folder_by_name(root_folder_name)

        for folder_name in parsed_path.relative_to(root_folder_name).parts:
            current_folder = self._folder_repository.get_by_name_and_parent_id(
                folder_name, current_folder.id
            )
            if current_folder is None:
                raise ValueError("Folder not found")

        return current_folder

    def add_folder_for_user(self, path: str, user_id: uuid.UUID):
        parsed_path = self._parse_path(path)
        filename = parsed_path.name
        parent_path = parsed_path.parent
        parent = self.get_folder_by_path(str(parent_path))
        new_folder = db_models.FolderEntity(
            name=filename, parent_folder=parent, owner_id=user_id
        )
        self._folder_repository.save(new_folder)

    def create_root_folder_for_user(self, user_id: uuid.UUID):
        folder_name = str(user_id)
        self._folder_repository.save(
            db_models.FolderEntity(name=folder_name, owner_id=user_id)
        )

    def get_folder_contents(
        self, path: str
    ) -> List[db_models.FolderEntity | db_models.FileEntity]:
        parsed_path = self._parse_path(path)
        contents = []
        folder = self.get_folder_by_path(str(parsed_path))

        contents += folder.subfolders
        contents += folder.files

        return contents

    def _parse_path(self, path: str) -> pathlib.PurePosixPath:
        parsed_path = pathlib.PurePosixPath(path)

        if parsed_path.is_absolute():
            parsed_path = parsed_path.relative_to("/")

        if len(parsed_path.parts) == 0:
            raise ValueError("Invalid path format")

        return parsed_path

    def _get_root_folder_by_name(self, name: str) -> db_models.FolderEntity:
        folder = self._folder_repository.get_by_name_and_parent_id(name, None)
        if folder:
            return folder
        raise ValueError("Folder not found")  # TODO: custom error
