from skylock.api import models
from skylock.database import models as db_models
from skylock.utils.path import UserPath


class ResponseBuilder:
    def get_folder_contents_response(
        self, folder: db_models.FolderEntity, user_path: UserPath
    ) -> models.FolderContents:
        parent_path = f"/{user_path.path}" if user_path.path else ""
        children_files = [
            models.File(
                name=file.name,
                is_public=file.is_public,
                path=f"{parent_path}/{file.name}",
            )
            for file in folder.files
        ]
        children_folders = [
            models.Folder(
                name=folder.name,
                is_public=folder.is_public,
                path=f"{parent_path}/{folder.name}",
            )
            for folder in folder.subfolders
        ]
        return models.FolderContents(files=children_files, folders=children_folders)

    def get_folder_response(
        self, folder: db_models.FolderEntity, user_path: UserPath
    ) -> models.Folder:
        return models.Folder(
            name=folder.name, path=f"/{user_path.path}", is_public=folder.is_public
        )

    def get_file_response(self, file: db_models.FileEntity, user_path: UserPath) -> models.File:
        return models.File(name=file.name, path=f"/{user_path.path}", is_public=file.is_public)
