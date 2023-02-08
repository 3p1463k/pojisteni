import pytest
from fastapi.testclient import TestClient
from sqlmodel import create_engine
from sqlmodel import Session
from sqlmodel import SQLModel
from sqlmodel.pool import StaticPool
from utils.users import authentication_token_from_email

from core.config import settings
from db.session import get_session
from main import app


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="normal_user_token_headers")
def normal_user_token_headers(client: client_fixture, session: session_fixture):

    """Get a valid JWT token for request"""

    return authentication_token_from_email(
        session,
        client,
        email=settings.TEST_USER_EMAIL,
        password=settings.TEST_USER_PASSWORD,
    )


@pytest.fixture(name="admin_token_headers")
def admin_token_headers(client: client_fixture, session: session_fixture):

    """Get a valid JWT token for request"""

    return authentication_token_from_email(
        session, client, email=settings.ADMIN_EMAIL, password=settings.ADMIN_PASSWORD
    )
