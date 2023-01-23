import os
import sys
from typing import Any
from typing import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# cesta pro import z db a main.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.base import Base
from db.session import get_db
from apis.base import api_router


def start_application():

    """Vytvorime instanci FASTAPI"""

    app = FastAPI()
    app.include_router(api_router)
    return app


"""Vytvorime SQLite databazi pro testovani"""

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def app() -> Generator[FastAPI, Any, None]:

    """Vytvorime novou databazi pro kazdy novy test"""

    Base.metadata.create_all(engine)  # Create the tables.
    _app = start_application()
    yield _app
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def db_session(app: FastAPI) -> Generator[SessionTesting, Any, None]:

    """Vytvorime session ........TODO"""

    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(
    app: FastAPI, db_session: SessionTesting
) -> Generator[TestClient, Any, None]:

    """Vytvorime FastAPI TestClient pouzijeme nasi db_session"""

    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    """Pro test prepiseme dependency injection v nasich routes"""

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client
