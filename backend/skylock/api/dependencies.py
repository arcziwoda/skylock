from fastapi import Depends

from skylock.database.models import UserEntity
from skylock.database.repository import FileRepository, FolderRepository, UserRepository
from skylock.database.session import get_db_session
from skylock.service.resource_service import ResourceService
from skylock.service.user_service import UserService
from skylock.skylock_facade import SkylockFacade
from skylock.utils.security import get_user_from_jwt, oauth2_scheme


def get_user_repository(db=Depends(get_db_session)) -> UserRepository:
    return UserRepository(db)


def get_folder_repository(db=Depends(get_db_session)) -> FolderRepository:
    return FolderRepository(db)


def get_file_repository(db=Depends(get_db_session)) -> FileRepository:
    return FileRepository(db)


def get_user_service(user_repository=Depends(get_user_repository)) -> UserService:
    return UserService(user_repository)


def get_resource_service(
    file_repository=Depends(get_file_repository),
    folder_repository=Depends(get_folder_repository),
) -> ResourceService:
    return ResourceService(
        file_repository=file_repository, folder_repository=folder_repository
    )


def get_skylock_facade(
    user_service: UserService = Depends(get_user_service),
    resource_service: ResourceService = Depends(get_resource_service),
) -> SkylockFacade:
    return SkylockFacade(user_service=user_service, resource_service=resource_service)


def get_current_user(
    token: str = Depends(oauth2_scheme), user_repository=Depends(get_user_repository)
) -> UserEntity:
    return get_user_from_jwt(token=token, user_repository=user_repository)
