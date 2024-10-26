import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker
from skylock.app import app
from skylock.database.models import Base
from skylock.database.repository import UserRepository
from skylock.service.user_service import UserService
from skylock.api.dependencies import get_user_service

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
def test_app(user_service):
    app.dependency_overrides[get_user_service] = lambda: user_service
    return app


@pytest.fixture
def client(test_app):
    with TestClient(test_app) as c:
        yield c
