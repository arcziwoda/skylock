from skylock.service.resource_service import ResourceService
from skylock.service.user_service import UserService
from skylock.api import models


class SkylockFacade:
    def __init__(self, user_service: UserService, resource_service: ResourceService):
        self._user_service = user_service
        self._resource_service = resource_service

    def register_user(self, username: str, password: str):
        user = self._user_service.register_user(username, password)
        self._resource_service.create_root_folder_for_user(user.id)

    def login_user(self, username: str, password: str) -> models.Token:
        return self._user_service.login_user(username, password)

    def create_folder_for_user(self, path: str, user: models.User):
        user_path = user.id + "/" + path
        self._resource_service.create_folder_for_user(user_path, user.id)
