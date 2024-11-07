from fastapi import APIRouter, Depends, UploadFile

from skylock.api.dependencies import get_current_user, get_skylock_facade
from skylock.api.validation import validate_path_not_empty
from skylock.database import models as db_models
from skylock.skylock_facade import SkylockFacade
from skylock.utils.path import UserPath

router = APIRouter(tags=["Resource"], prefix="/files")


@router.post("/upload/{path:path}")
def upload_file(
    file: UploadFile,
    path: str = Depends(validate_path_not_empty),
    user: db_models.UserEntity = Depends(get_current_user),
    skylock: SkylockFacade = Depends(get_skylock_facade),
):
    skylock.upload_file(user_path=UserPath(path=path, owner=user), file_data=file.file)
