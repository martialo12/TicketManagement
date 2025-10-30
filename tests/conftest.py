"""Test configuration and fixtures."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create test database FIRST
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# PATCH the engine BEFORE importing app
import app.core.database as db_module  # noqa: E402

db_module.engine = engine

# NOW import app and other dependencies
from fastapi.testclient import TestClient  # noqa: E402

from app.core.database import get_db  # noqa: E402
from app.main import app  # noqa: E402
from app.tickets.models import Base  # noqa: E402


@pytest.fixture
def db_session():
    """Create a fresh database session for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    """Create a test client with test database."""
    # Create tables with test engine (engine already patched at module level)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    # Override the database dependency
    app.dependency_overrides[get_db] = override_get_db

    # Create test client - startup event will now use test engine
    with TestClient(app, raise_server_exceptions=True) as test_client:
        yield test_client

    # Cleanup
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)
