from fastapi import APIRouter, Depends
from skylock.api import models
from skylock.database import models as db_models
from skylock.api.dependencies import get_resource_service
from skylock.service.resource_service import ResourceService
from skylock.utils.security import get_current_user

router = APIRouter(tags=["Resource"], prefix="/folders")


@router.post("{path:path}")
def create_folder(
    path: str,
    user: models.User = Depends(get_current_user),
    resource_service: ResourceService = Depends(get_resource_service),
):
    path = "/" + str(user.id) + path
    resource_service.add_folder_for_user(path, user.id)


@router.get("{path:path}")
def get_folder_contents(
    path: str,
    user: db_models.UserEntity = Depends(get_current_user),
    resource_service: ResourceService = Depends(get_resource_service),
):
    path = "/" + str(user.id) + path
    return resource_service.get_folder_contents(path)
