from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from .api.auth_routes import router as auth_router
from .repository.config.db_config import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(title="File Sharing API", version="1.0.0", lifespan=lifespan)


app.include_router(auth_router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(app)
