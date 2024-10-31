import pathlib

from fastapi import HTTPException

from skylock.utils.exceptions import InvalidPathException


class SkylockPath:
    def __init__(self, path: str, root_folder_name: str):
        self._path = self._parse_path(path)
        if not root_folder_name:
            raise InvalidPathException("Root folder cannot be empty")
        self._root_folder_name = root_folder_name

    @property
    def path(self) -> str:
        return str(self._path)

    @property
    def root_folder_name(self) -> str:
        return self._root_folder_name

    @property
    def parts(self) -> tuple[str, ...]:
        return self._path.parts

    @property
    def parent(self) -> "SkylockPath":
        if self.is_root_folder():
            raise HTTPException(403, "You cannot access parent of root folder")
        return SkylockPath(
            path=str(self._path.parent), root_folder_name=self._root_folder_name
        )

    @property
    def name(self) -> str:
        return str(self._path.name)

    def is_root_folder(self):
        return self._path == pathlib.PurePosixPath("")

    def _parse_path(self, path: str) -> pathlib.PurePosixPath:
        max_length = 255
        if len(str(path)) > max_length:
            raise InvalidPathException("Path length exceeds allowed maximum.")

        p = pathlib.PurePosixPath(path)

        if p.is_absolute():
            p = p.relative_to(p.root)

        return p
