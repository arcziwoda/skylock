from fastapi import APIRouter, Depends, status
from skylock.api import models
from skylock.api.dependencies import get_skylock_facade
from skylock.skylock_facade import SkylockFacade
from skylock.utils.security import get_current_user

router = APIRouter(tags=["Resource"], prefix="/folders")


@router.post(
    "{path:path}",
    status_code=status.HTTP_201_CREATED,
)
def create_folder(
    path: str,
    user: models.User = Depends(get_current_user),
    skylock: SkylockFacade = Depends(get_skylock_facade),
):
    skylock.create_folder_for_user(path, user)
    return "Folder created"
