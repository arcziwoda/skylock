from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from skylock.utils.exceptions import InvalidCredentialsException, UserAlreadyExists

async def user_already_exists_handler(request: Request, exc: UserAlreadyExists):
    return JSONResponse(
        status_code=409,
        content={"detail": str(exc)},
    )

async def invalid_credentials_handler(request: Request, exc: InvalidCredentialsException):
    return JSONResponse(
        status_code=401,
        content={"detail": "Invalid credentials provided"},
    )
