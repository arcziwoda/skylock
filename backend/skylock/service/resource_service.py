from typing import IO, Optional

from skylock.database import models as db_models
from skylock.database.repository import FileRepository, FolderRepository
from skylock.utils.exceptions import (
    FolderNotEmptyException,
    ForbiddenActionException,
    ResourceAlreadyExistsException,
    ResourceNotFoundException,
    RootFolderAlreadyExistsException,
)
from skylock.utils.path import UserPath
from skylock.utils.storage import delete_file_data, get_file_data, save_file_data


class ResourceService:
    def __init__(self, file_repository: FileRepository, folder_repository: FolderRepository):
        self._file_repository = file_repository
        self._folder_repository = folder_repository

    def get_folder(self, user_path: UserPath) -> db_models.FolderEntity:
        current_folder = self._get_root_folder_by_name(user_path.root_folder_name)

        if current_folder is None:
            raise LookupError(f"Root folder: {user_path.root_folder_name} does not exist")

        for folder_name in user_path.parts:
            current_folder = self._folder_repository.get_by_name_and_parent_id(
                folder_name, current_folder.id
            )
            if current_folder is None:
                raise ResourceNotFoundException(missing_resource_name=folder_name)

        return current_folder

    def get_folder_by_id(self, folder_id: str) -> db_models.FolderEntity:
        current_folder = self._folder_repository.get_by_id(folder_id)

        if current_folder is None:
            raise ResourceNotFoundException(missing_resource_name=folder_id)

        return current_folder

    def get_public_folder(self, folder_id: str) -> db_models.FolderEntity:
        folder = self.get_folder_by_id(folder_id)

        if not folder.is_public:
            raise ForbiddenActionException(f"Folder with id {folder_id} is not public")

        return folder

    def create_folder(self, user_path: UserPath) -> db_models.FolderEntity:
        if user_path.is_root_folder():
            raise ForbiddenActionException("Creation of root folder is forbidden")

        folder_name = user_path.name
        parent_path = user_path.parent
        parent = self.get_folder(parent_path)

        self._assert_no_children_matching_name(parent, folder_name)

        new_folder = db_models.FolderEntity(
            name=folder_name, parent_folder=parent, owner=user_path.owner
        )
        return self._folder_repository.save(new_folder)

    def delete_folder(self, user_path: UserPath, is_recursively: bool = False):
        folder = self.get_folder(user_path)
        self._delete_folder(folder, is_recursively=is_recursively)

    def update_folder(self, folder: db_models.FolderEntity):
        self._folder_repository.save(folder)

    def _delete_folder(self, folder: db_models.FolderEntity, is_recursively: bool = False):
        if folder.is_root():
            raise ForbiddenActionException("Deletion of root folder is forbidden")

        has_folder_children = bool(folder.subfolders or folder.files)
        if not is_recursively and has_folder_children:
            raise FolderNotEmptyException

        for file in folder.files:
            self._delete_file(file)

        for subfolder in folder.subfolders:
            self._delete_folder(subfolder, is_recursively=True)

        self._folder_repository.delete(folder)

    def get_file(self, user_path: UserPath) -> db_models.FileEntity:
        parent_folder = self.get_folder(user_path.parent)
        file = self._file_repository.get_by_name_and_parent(
            name=user_path.name, parent=parent_folder
        )

        if file is None:
            raise ResourceNotFoundException(missing_resource_name=user_path.name)

        if file.owner_id != user_path.owner.id:
            raise ForbiddenActionException("You do not have access to ths file")

        return file

    def get_file_by_id(self, file_id: str) -> db_models.FileEntity:
        file = self._file_repository.get_by_id(file_id)

        if file is None:
            raise ResourceNotFoundException(missing_resource_name=file_id)

        return file

    def create_file(
        self, user_path: UserPath, data: IO[bytes], force: bool = False, public: bool = False
    ) -> db_models.FileEntity:
        if not user_path.name:
            raise ForbiddenActionException("Creation of file with no name is forbidden")

        file_name = user_path.name
        parent_path = user_path.parent
        parent = self.get_folder(parent_path)

        if force:
            try:
                self.delete_file(user_path)
            except ResourceNotFoundException:
                pass

        self._assert_no_children_matching_name(parent, file_name)

        new_file = self._file_repository.save(
            db_models.FileEntity(
                name=file_name, folder=parent, owner=user_path.owner, is_public=public
            )
        )

        self._save_file_data(file=new_file, data=data)

        return new_file

    def update_file(self, file: db_models.FileEntity):
        self._file_repository.save(file)

    def delete_file(self, user_path: UserPath):
        file = self.get_file(user_path)
        self._delete_file(file)

    def _delete_file(self, file: db_models.FileEntity):
        self._file_repository.delete(file)
        self._delete_file_data(file)

    def get_file_data(self, user_path: UserPath) -> IO[bytes]:
        file = self.get_file(user_path)
        return self._get_file_data(file)

    def get_public_file_data(self, file_id: str) -> IO[bytes]:
        file = self.get_file_by_id(file_id)

        if not file.is_public:
            raise ForbiddenActionException(f"File with id {id} is not public")

        return self._get_file_data(file)

    def _save_file_data(self, file: db_models.FileEntity, data: IO[bytes]):
        save_file_data(data=data, filename=file.id)

    def _get_file_data(self, file: db_models.FileEntity) -> IO[bytes]:
        return get_file_data(filename=file.id)

    def _delete_file_data(self, file: db_models.FileEntity):
        return delete_file_data(file.id)

    def create_root_folder(self, user_path: UserPath):
        if not user_path.is_root_folder():
            raise ValueError("Given path is not a proper root folder path")
        if self._get_root_folder_by_name(user_path.root_folder_name):
            raise RootFolderAlreadyExistsException("This root folder already exists")
        self._folder_repository.save(
            db_models.FolderEntity(name=user_path.root_folder_name, owner=user_path.owner)
        )

    def _get_root_folder_by_name(self, name: str) -> Optional[db_models.FolderEntity]:
        return self._folder_repository.get_by_name_and_parent_id(name, None)

    def _assert_no_children_matching_name(self, folder: db_models.FolderEntity, name: str):
        exists_file_of_name = name in [file.name for file in folder.files]
        exists_folder_of_name = name in [folder.name for folder in folder.subfolders]
        if exists_file_of_name or exists_folder_of_name:
            raise ResourceAlreadyExistsException
