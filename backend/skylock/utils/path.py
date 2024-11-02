import pathlib


from skylock.utils.exceptions import ForbiddenActionException, InvalidPathException


class SkylockPath:
    def __init__(self, path: str, root_folder_name: str):
        self._parsed_path = self._validate_and_parse_path(path)
        if not root_folder_name:
            raise InvalidPathException("Root folder cannot be empty")
        self._root_folder_name = root_folder_name

    @property
    def path(self) -> str:
        return str(self._parsed_path).replace(".", "")

    @property
    def root_folder_name(self) -> str:
        return self._root_folder_name

    @property
    def parts(self) -> tuple[str, ...]:
        return self._parsed_path.parts

    @property
    def parent(self) -> "SkylockPath":
        if self.is_root_folder():
            raise ForbiddenActionException("You cannot access parent of root folder")
        return SkylockPath(
            path=str(self._parsed_path.parent), root_folder_name=self._root_folder_name
        )

    @property
    def name(self) -> str:
        return str(self._parsed_path.name)

    def is_root_folder(self):
        return self._parsed_path == pathlib.PurePosixPath("")

    def _validate_and_parse_path(self, initial_path: str) -> pathlib.PurePosixPath:
        max_length = 255
        if len(str(initial_path)) > max_length:
            raise InvalidPathException("Path length exceeds allowed maximum.")

        parsed_path = pathlib.PurePosixPath(initial_path)

        if parsed_path.is_absolute():
            parsed_path = parsed_path.relative_to(parsed_path.root)

        return parsed_path
