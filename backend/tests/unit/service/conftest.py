import pytest
from unittest.mock import MagicMock, patch
from skylock.service.path_resolver import PathResolver
from skylock.service.resource_service import ResourceService


@pytest.fixture
def mock_file_repository():
    return MagicMock()


@pytest.fixture
def mock_folder_repository():
    return MagicMock()


@pytest.fixture
def mock_user_repository():
    return MagicMock()


@pytest.fixture
def path_resolver(mock_file_repository, mock_folder_repository, mock_user_repository):
    return PathResolver(
        file_repository=mock_file_repository,
        folder_repository=mock_folder_repository,
        user_repository=mock_user_repository,
    )


@pytest.fixture
def resource_service(mock_file_repository, mock_folder_repository, path_resolver):
    return ResourceService(
        file_repository=mock_file_repository,
        folder_repository=mock_folder_repository,
        path_resolver=path_resolver,
    )
