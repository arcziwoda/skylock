from fastapi import Depends

from skylock.database.models import UserEntity
from skylock.database.repository import FileRepository, FolderRepository, UserRepository
from skylock.database.session import get_db_session
from skylock.service.path_resolver import PathResolver
from skylock.service.resource_service import ResourceService
from skylock.service.response_builder import ResponseBuilder
from skylock.service.user_service import UserService
from skylock.skylock_facade import SkylockFacade
from skylock.utils.security import get_user_from_jwt, oauth2_scheme
from skylock.utils.url_generator import UrlGenerator


def get_user_repository(db=Depends(get_db_session)) -> UserRepository:
    return UserRepository(db)


def get_folder_repository(db=Depends(get_db_session)) -> FolderRepository:
    return FolderRepository(db)


def get_file_repository(db=Depends(get_db_session)) -> FileRepository:
    return FileRepository(db)


def get_user_service(user_repository=Depends(get_user_repository)) -> UserService:
    return UserService(user_repository)


def get_path_resolver(
    file_repository=Depends(get_file_repository),
    folder_repository=Depends(get_folder_repository),
    user_repository=Depends(get_user_repository),
) -> PathResolver:
    return PathResolver(
        file_repository=file_repository,
        folder_repository=folder_repository,
        user_repository=user_repository,
    )


def get_resource_service(
    file_repository=Depends(get_file_repository),
    folder_repository=Depends(get_folder_repository),
    path_resolver=Depends(get_path_resolver),
) -> ResourceService:
    return ResourceService(
        file_repository=file_repository,
        folder_repository=folder_repository,
        path_resolver=path_resolver,
    )


def get_skylock_facade(
    user_service=Depends(get_user_service),
    resource_service=Depends(get_resource_service),
    path_resolver=Depends(get_path_resolver),
) -> SkylockFacade:
    return SkylockFacade(
        user_service=user_service,
        resource_service=resource_service,
        url_generator=UrlGenerator(),
        path_resolver=path_resolver,
        response_builder=ResponseBuilder(),
    )


def get_current_user(
    token: str = Depends(oauth2_scheme), user_repository=Depends(get_user_repository)
) -> UserEntity:
    return get_user_from_jwt(token=token, user_repository=user_repository)
