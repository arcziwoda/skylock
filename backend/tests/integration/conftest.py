import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

from skylock.api.dependencies import get_current_user, get_skylock_facade
from skylock.app import app
from skylock.api.app import api
from skylock.database.models import Base, UserEntity
from skylock.database.repository import FileRepository, FolderRepository, UserRepository
from skylock.database.session import get_db_session
from skylock.service.path_resolver import PathResolver
from skylock.service.resource_service import ResourceService
from skylock.service.response_builder import ResponseBuilder
from skylock.service.user_service import UserService
from skylock.skylock_facade import SkylockFacade
from skylock.utils.path import UserPath
from skylock.utils.url_generator import UrlGenerator

TEST_DATABASE_URL = "sqlite://"

MOCK_USERNAME = "mockuser"
MOCK_PASSWORD = "mockpasswd"


@pytest.fixture
def db_session():
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

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
def path_resolver(file_repository, folder_repository, user_repository):
    return PathResolver(
        file_repository=file_repository,
        folder_repository=folder_repository,
        user_repository=user_repository,
    )


@pytest.fixture
def resource_service(file_repository, folder_repository, path_resolver):
    return ResourceService(
        file_repository=file_repository,
        folder_repository=folder_repository,
        path_resolver=path_resolver,
    )


@pytest.fixture
def skylock(user_service, resource_service, path_resolver):
    return SkylockFacade(
        user_service=user_service,
        resource_service=resource_service,
        url_generator=UrlGenerator(),
        path_resolver=path_resolver,
        response_builder=ResponseBuilder(),
    )


@pytest.fixture
def mock_user(db_session, resource_service):
    user = UserEntity(
        username=MOCK_USERNAME,
        password=MOCK_PASSWORD,
    )
    db_session.add(user)
    db_session.commit()

    resource_service.create_root_folder(UserPath.root_folder_of(user))
    return user


@pytest.fixture
def test_app(skylock, db_session, mock_user):
    api.dependency_overrides[get_skylock_facade] = lambda: skylock
    api.dependency_overrides[get_db_session] = lambda: db_session
    api.dependency_overrides[get_current_user] = lambda: mock_user
    return api


@pytest.fixture
def client(test_app):
    with TestClient(test_app) as c:
        yield c
