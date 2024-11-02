import pytest
import pathlib
from skylock.utils.exceptions import ForbiddenActionException, InvalidPathException
from skylock.utils.path import SkylockPath


def test_init_valid_path():
    path = SkylockPath(path="some/path", root_folder_name="root")
    assert path.path == "some/path"
    assert path.root_folder_name == "root"


def test_init_empty_root_folder_name():
    with pytest.raises(InvalidPathException):
        SkylockPath(path="some/path", root_folder_name="")


def test_path_property():
    path = SkylockPath(path="some/path", root_folder_name="root")
    assert path.path == "some/path"


def test_root_folder_name_property():
    path = SkylockPath(path="some/path", root_folder_name="root")
    assert path.root_folder_name == "root"


def test_parts_property():
    path = SkylockPath(path="some/path", root_folder_name="root")
    assert path.parts == ("some", "path")


def test_parent_property():
    path = SkylockPath(path="some/path", root_folder_name="root")
    parent_path = path.parent
    assert parent_path.path == "some"
    assert parent_path.root_folder_name == "root"


def test_parent_property_root_folder():
    path = SkylockPath(path="", root_folder_name="root")
    with pytest.raises(ForbiddenActionException):
        _ = path.parent


def test_name_property():
    path = SkylockPath(path="some/path", root_folder_name="root")
    assert path.name == "path"


def test_is_root_folder():
    path = SkylockPath(path="", root_folder_name="root")
    assert path.is_root_folder()


def test_parse_path_valid():
    path = SkylockPath(path="some/path", root_folder_name="root")
    assert path._validate_and_parse_path("some/path") == pathlib.PurePosixPath(
        "some/path"
    )


def test_parse_path_exceeds_max_length():
    long_path = "a" * 256
    with pytest.raises(InvalidPathException):
        SkylockPath(path=long_path, root_folder_name="root")


def test_parse_path_absolute():
    path = SkylockPath(path="/some/path", root_folder_name="root")
    assert path._validate_and_parse_path("/some/path") == pathlib.PurePosixPath(
        "some/path"
    )
