import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker
from skylock.app import app
from skylock.database.models import Base
from skylock.database.repository import FileRepository, FolderRepository, UserRepository
from skylock.service.resource_service import ResourceService
from skylock.service.user_service import UserService
from skylock.api.dependencies import get_skylock_facade
from skylock.skylock_facade import SkylockFacade

TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture
def db_session():
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = factory()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def user_repository(db_session):
    return UserRepository(db_session)


@pytest.fixture
def user_service(user_repository):
    return UserService(user_repository)


@pytest.fixture
def folder_repository(db_session):
    return FolderRepository(db_session)


@pytest.fixture
def file_repository(db_session):
    return FileRepository(db_session)


@pytest.fixture
def resource_service(file_repository, folder_repository):
    return ResourceService(
        file_repository=file_repository, folder_repository=folder_repository
    )


@pytest.fixture
def skylock(user_service, resource_service):
    return SkylockFacade(user_service=user_service, resource_service=resource_service)


@pytest.fixture
def test_app(skylock):
    app.dependency_overrides[get_skylock_facade] = lambda: skylock
    return app


@pytest.fixture
def client(test_app):
    with TestClient(test_app) as c:
        yield c
