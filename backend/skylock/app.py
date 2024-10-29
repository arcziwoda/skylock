from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from skylock.api import auth_routes, folder_routes
from skylock.utils.exceptions import InvalidCredentialsException, UserAlreadyExists

app = FastAPI(title="File Sharing API", version="1.0.0", root_path="/api/v1")


@app.exception_handler(UserAlreadyExists)
def user_already_exists_handler(_request: Request, exc: UserAlreadyExists):
    return JSONResponse(
        status_code=409,
        content={"detail": str(exc)},
    )


@app.exception_handler(InvalidCredentialsException)
def invalid_credentials_handler(_request: Request, _exc: InvalidCredentialsException):
    return JSONResponse(
        status_code=401,
        content={"detail": "Invalid credentials provided"},
    )


app.include_router(auth_routes.router)
app.include_router(folder_routes.router)
