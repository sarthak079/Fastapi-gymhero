import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session, pool
from app.main import app
from app.database import get_session

# 1. Create an in-memory SQLite database for testing
# "StaticPool" is important for in-memory databases to maintain the same thread connection
TEST_DATABASE_URL = "sqlite:///:memory:"
engine=create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=pool.StaticPool)

def override_get_session():
    with Session(engine) as session:
        yield session

app.dependency_overrides[get_session] = override_get_session
@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(bind=engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(bind=engine)

@pytest.fixture(name="client")
def client_fixture(session:Session):
    def get_test_override():
        yield session
    
    app.dependency_overrides[get_session] = get_test_override
    client = TestClient(app)
    yield client

    app.dependency_overrides.clear()