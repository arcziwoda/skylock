from fastapi import APIRouter, Depends, HTTPException, status

from ..dependencies import get_user_service
from ..exceptions import InvalidCredentialsException, UserAlreadyExists
from ..service.user_service import UserService
from .model.login_user_request import LoginUserRequest
from .model.register_user_request import RegisterUserRequest
from .model.token_response import TokenResponse

router = APIRouter()


@router.post("/auth/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    request: RegisterUserRequest, user_service: UserService = Depends(get_user_service)
):
    try:
        user_service.register_user(username=request.username, password=request.password)
        return {"message": "User registered successfully"}
    except UserAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.post("/auth/login")
async def login_user(
    request: LoginUserRequest, user_service: UserService = Depends(get_user_service)
):
    try:
        token = user_service.verify_user(
            username=request.username, password=request.password
        )
        return TokenResponse(access_token=token, token_type="bearer")
    except InvalidCredentialsException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
