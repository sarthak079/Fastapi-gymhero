import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from app.main import app
from app.database import get_session

DATABASE_URL = "sqlite:///./test_database.db"
engine=create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

def override_get_session():
    with Session(engine) as session:
        yield session

app.dependency_overrides[get_session] = override_get_session
@pytest.fixture(name="client")
def client():
    SQLModel.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    SQLModel.metadata.drop_all(bind=engine)