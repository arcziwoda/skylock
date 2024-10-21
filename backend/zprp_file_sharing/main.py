from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn

from .repository.config.db_config import create_tables
from .api.auth_routes import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(title="File Sharing API", version="1.0.0", lifespan=lifespan)


app.include_router(auth_router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(app)
