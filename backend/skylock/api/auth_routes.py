from fastapi import APIRouter, Depends, HTTPException, status

from skylock.service.model.user import User

from skylock.core.dependencies import get_user_service
from skylock.core.exceptions import InvalidCredentialsException, UserAlreadyExists
from skylock.service.user_service import UserService
from skylock.api.model.login_user_request import LoginUserRequest
from skylock.api.model.register_user_request import RegisterUserRequest
from skylock.service.model.token import Token

router = APIRouter(tags=["Auth"], prefix="/auth")


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="This endpoint allows a new user to register with a unique username and password. If the username already exists, a 409 Conflict error will be raised.",
    responses={
        201: {"description": "User successfully registered"},
        409: {"description": "User with the provided username already exists"},
    },
)
def register_user(
    request: RegisterUserRequest, user_service: UserService = Depends(get_user_service)
) -> User:
    try:
        return user_service.register_user(
            username=request.username, password=request.password
        )
    except UserAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.post(
    "/login",
    response_model=Token,
    summary="Authenticate user and get JWT token",
    description="This endpoint allows an existing user to authenticate using their username and password. A JWT token is returned if the credentials are valid.",
    responses={
        200: {"description": "Successful login, JWT token returned"},
        401: {"description": "Invalid credentials provided"},
    },
)
def login_user(
    request: LoginUserRequest, user_service: UserService = Depends(get_user_service)
) -> Token:
    try:
        return user_service.login_user(
            username=request.username, password=request.password
        )
    except InvalidCredentialsException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
