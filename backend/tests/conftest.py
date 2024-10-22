import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from skylock.main import app
from skylock.repository.config import Base
from skylock.repository.user_repository import UserRepository
from skylock.service.user_service import UserService

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def user_repository(db_session):
    return UserRepository(db_session=db_session)


@pytest.fixture(scope="function")
def user_service(user_repository):
    return UserService(user_repository=user_repository)


@pytest.fixture(scope="function")
def client():
    with TestClient(app) as test_client:
        yield test_client
