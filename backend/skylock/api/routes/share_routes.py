from typing import Annotated

from fastapi import APIRouter, Depends
from skylock.database import models as db_models
from skylock.api.dependencies import get_skylock_facade, get_current_user
from skylock.api.validation import validate_path_not_empty
from skylock.skylock_facade import SkylockFacade
from skylock.utils.path import UserPath
from skylock.api import models

router = APIRouter(tags=["Resource"], prefix="/share")


@router.get("/folders/{path:path}")
def get_folder_url(
    path: Annotated[str, Depends(validate_path_not_empty)],
    user: Annotated[db_models.UserEntity, Depends(get_current_user)],
    skylock: Annotated[SkylockFacade, Depends(get_skylock_facade)],
):
    url = skylock.get_folder_url(UserPath(path=path, owner=user))
    return models.ResourceLocationResponse(location=url)


@router.get("/files/{path:path}")
def get_file_url(
    path: Annotated[str, Depends(validate_path_not_empty)],
    user: Annotated[db_models.UserEntity, Depends(get_current_user)],
    skylock: Annotated[SkylockFacade, Depends(get_skylock_facade)],
):
    url = skylock.get_file_url(UserPath(path=path, owner=user))
    return models.ResourceLocationResponse(location=url)
