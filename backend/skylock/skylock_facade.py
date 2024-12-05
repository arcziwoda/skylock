from typing import IO


from skylock.service.path_resolver import PathResolver
from skylock.service.resource_service import ResourceService
from skylock.service.response_builder import ResponseBuilder
from skylock.service.user_service import UserService
from skylock.api import models
from skylock.utils.exceptions import ForbiddenActionException
from skylock.utils.path import UserPath
from skylock.utils.url_generator import UrlGenerator


class SkylockFacade:
    def __init__(
        self,
        user_service: UserService,
        resource_service: ResourceService,
        path_resolver: PathResolver,
        url_generator: UrlGenerator,
        response_builder: ResponseBuilder,
    ):
        self._user_service = user_service
        self._resource_service = resource_service
        self._path_resolver = path_resolver
        self._url_generator = url_generator
        self._response_builder = response_builder

    def register_user(self, username: str, password: str):
        user = self._user_service.register_user(username, password)
        self._resource_service.create_root_folder(UserPath.root_folder_of(user))

    def login_user(self, username: str, password: str) -> models.Token:
        return self._user_service.login_user(username, password)

    def create_folder_for_user(
        self, user_path: UserPath, with_parents: bool = False
    ) -> models.Folder:
        if with_parents:
            folder = self._resource_service.create_folder_with_parents(user_path=user_path)
        else:
            folder = self._resource_service.create_folder(user_path=user_path)

        return self._response_builder.get_folder_response(folder=folder, user_path=user_path)

    def get_folder_contents(self, user_path: UserPath) -> models.FolderContents:
        folder = self._resource_service.get_folder(user_path)
        return self._response_builder.get_folder_contents_response(
            folder=folder, user_path=user_path
        )

    def get_public_folder_contents(self, folder_id: str) -> models.FolderContents:
        folder = self._resource_service.get_public_folder(folder_id)
        path = self._path_resolver.path_from_folder(folder)
        return self._response_builder.get_folder_contents_response(folder=folder, user_path=path)

    def delete_folder(self, user_path: UserPath, is_recursively: bool = False):
        if user_path.is_root_folder():
            raise ForbiddenActionException("Deletion of root folder is forbidden")
        self._resource_service.delete_folder(user_path, is_recursively=is_recursively)

    def update_folder_visability(self, user_path: UserPath, is_public: bool) -> models.Folder:
        folder = self._resource_service.update_folder_visibility(user_path, is_public)
        return self._response_builder.get_folder_response(folder=folder, user_path=user_path)

    def update_file_visability(self, user_path: UserPath, is_public: bool) -> models.File:
        file = self._resource_service.update_file_visibility(user_path, is_public)
        return self._response_builder.get_file_response(file=file, user_path=user_path)

    def upload_file(
        self, user_path: UserPath, file_data: IO[bytes], force: bool = False, public: bool = False
    ) -> models.File:
        file = self._resource_service.create_file(user_path, file_data, force, public)
        return self._response_builder.get_file_response(file=file, user_path=user_path)

    def download_file(self, user_path: UserPath) -> IO[bytes]:
        return self._resource_service.get_file_data(user_path)

    def download_public_file(self, file_id: str) -> IO[bytes]:
        return self._resource_service.get_public_file_data(file_id)

    def delete_file(self, user_path: UserPath):
        self._resource_service.delete_file(user_path)

    def get_folder_url(self, user_path: UserPath) -> str:
        folder = self._resource_service.get_folder(user_path)
        return self._url_generator.generate_url_for_folder(folder.id)

    def get_file_url(self, user_path: UserPath) -> str:
        file = self._resource_service.get_file(user_path)
        return self._url_generator.generate_url_for_file(file.id)
