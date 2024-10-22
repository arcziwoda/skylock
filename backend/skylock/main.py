from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from skylock.api.auth_routes import router as auth_router
from skylock.repository.config import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(
    title="File Sharing API", version="1.0.0", lifespan=lifespan, root_path="/api/v1"
)


app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")
