from fastapi import FastAPI
from skylock.utils.exception_handlers import (
    folder_not_empty_handler,
    forbidden_action_handler,
    resource_not_found_handler,
    user_already_exists_handler,
    resource_already_exists_handler,
    invalid_credentials_handler,
)

from skylock.api.routes import auth_routes, folder_routes, file_routes, public_routes, share_routes
from skylock.utils.exceptions import (
    FolderNotEmptyException,
    InvalidCredentialsException,
    ResourceAlreadyExistsException,
    ResourceNotFoundException,
    UserAlreadyExists,
    ForbiddenActionException,
)
from skylock.pages import page_router

app = FastAPI(title="File Sharing API", version="1.0.0")


app.add_exception_handler(UserAlreadyExists, user_already_exists_handler)
app.add_exception_handler(InvalidCredentialsException, invalid_credentials_handler)
app.add_exception_handler(ResourceAlreadyExistsException, resource_already_exists_handler)
app.add_exception_handler(ResourceNotFoundException, resource_not_found_handler)
app.add_exception_handler(FolderNotEmptyException, folder_not_empty_handler)
app.add_exception_handler(ForbiddenActionException, forbidden_action_handler)


app.include_router(auth_routes.router, prefix="/api/v1")
app.include_router(folder_routes.router, prefix="/api/v1")
app.include_router(file_routes.router, prefix="/api/v1")
app.include_router(public_routes.router, prefix="/api/v1")
app.include_router(share_routes.router, prefix="/api/v1")
app.include_router(page_router.router)
