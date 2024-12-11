import pathlib
import shutil
from io import BytesIO
from typing import IO

from skylock.database import models as db_models

FILES_FOLDER_DISK_PATH = "./data/files"


class FileStorageService:
    def __init__(self, storage_path: str = FILES_FOLDER_DISK_PATH):
        self.storage_path = pathlib.Path(storage_path)

    def _ensure_files_folder(self) -> pathlib.Path:
        self.storage_path.mkdir(parents=True, exist_ok=True)
        return self.storage_path

    def save_file(self, data: bytes, file: db_models.FileEntity) -> None:
        filename = self._get_filename(file)

        folder = self._ensure_files_folder()
        path = folder / filename

        if path.exists():
            raise ValueError(f"File of given path: {path} already exists")

        with path.open("wb") as buffer:
            shutil.copyfileobj(BytesIO(data), buffer)

    def get_file(self, file: db_models.FileEntity) -> IO[bytes]:
        filename = self._get_filename(file)

        folder = self._ensure_files_folder()
        path = folder / filename

        if not path.exists():
            raise ValueError(f"File of given path: {path} does not exist")

        return BytesIO(path.read_bytes())

    def delete_file(self, file: db_models.FileEntity) -> None:
        filename = self._get_filename(file)

        folder = self._ensure_files_folder()
        path = folder / filename

        if not path.exists():
            raise ValueError(f"File of given path: {path} does not exist")

        path.unlink()

    def _get_filename(self, file: db_models.FileEntity) -> str:
        return file.id
