import pathlib
import shutil
from typing import IO


FILES_FOLDER_DISK_PATH = "./data/files"


def save_file_data(file: IO[bytes], filename: str):
    folder = create_files_folder_if_non_existent()

    path = folder / filename

    if path.exists():
        raise ValueError(f"File of given path: {path} already exists")

    with path.open("wb") as buffer:
        shutil.copyfileobj(file, buffer)


def create_files_folder_if_non_existent() -> pathlib.Path:
    folder = pathlib.Path(FILES_FOLDER_DISK_PATH)
    folder.mkdir(parents=True, exist_ok=True)
    return folder
