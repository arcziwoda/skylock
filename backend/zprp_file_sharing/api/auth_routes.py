from fastapi import APIRouter, Depends, HTTPException, status
from typing import Any

from ..core.dependencies import get_user_service
from ..core.exceptions import InvalidCredentialsException, UserAlreadyExists
from ..service.user_service import UserService
from .model.login_user_request import LoginUserRequest
from .model.register_user_request import RegisterUserRequest
from .model.token_response import TokenResponse

router = APIRouter(tags=["Auth"])


@router.post(
    "/auth/register",
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="This endpoint allows a new user to register with a unique username and password. If the username already exists, a 409 Conflict error will be raised.",
    responses={
        201: {"description": "User successfully registered"},
        409: {"description": "User with the provided username already exists"},
    },
)
async def register_user(
    request: RegisterUserRequest, user_service: UserService = Depends(get_user_service)
) -> Any:
    try:
        user_service.register_user(username=request.username, password=request.password)
        return {"message": "User registered successfully"}
    except UserAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.post(
    "/auth/login",
    response_model=TokenResponse,
    summary="Authenticate user and get JWT token",
    description="This endpoint allows an existing user to authenticate using their username and password. A JWT token is returned if the credentials are valid.",
    responses={
        200: {"description": "Successful login, JWT token returned"},
        401: {"description": "Invalid credentials provided"},
    },
)
async def login_user(
    request: LoginUserRequest, user_service: UserService = Depends(get_user_service)
) -> TokenResponse:
    try:
        token = user_service.verify_user(
            username=request.username, password=request.password
        )
        return TokenResponse(access_token=token, token_type="bearer")
    except InvalidCredentialsException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
