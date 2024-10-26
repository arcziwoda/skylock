from fastapi import FastAPI

from skylock.api import auth_routes
from skylock.utils.exception_handlers import (
    UserAlreadyExists,
    InvalidCredentialsException,
)
from skylock.utils.exception_handlers import (
    user_already_exists_handler,
    invalid_credentials_handler,
)


app = FastAPI(title="File Sharing API", version="1.0.0", root_path="/api/v1")

app.add_exception_handler(UserAlreadyExists, user_already_exists_handler)
app.add_exception_handler(InvalidCredentialsException, invalid_credentials_handler)

app.include_router(auth_routes.router)
