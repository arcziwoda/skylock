from fastapi import FastAPI
from skylock.utils.exception_handlers import (
    folder_not_empty_handler,
    forbidden_action_handler,
    resource_not_found_handler,
    user_already_exists_handler,
    resource_already_exists_handler,
    invalid_credentials_handler,
)

from skylock.api import auth_routes, folder_routes
from skylock.utils.exceptions import (
    FolderNotEmptyException,
    InvalidCredentialsException,
    ResourceAlreadyExistsException,
    ResourceNotFoundException,
    UserAlreadyExists,
    ForbiddenActionException,
)

app = FastAPI(title="File Sharing API", version="1.0.0", root_path="/api/v1")


app.add_exception_handler(UserAlreadyExists, user_already_exists_handler)
app.add_exception_handler(InvalidCredentialsException, invalid_credentials_handler)
app.add_exception_handler(
    ResourceAlreadyExistsException, resource_already_exists_handler
)
app.add_exception_handler(ResourceNotFoundException, resource_not_found_handler)
app.add_exception_handler(FolderNotEmptyException, folder_not_empty_handler)
app.add_exception_handler(ForbiddenActionException, forbidden_action_handler)


app.include_router(auth_routes.router)
app.include_router(folder_routes.router)
