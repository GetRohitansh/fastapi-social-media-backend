import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import Settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db, Base
import pytest


# SQL_ALCHEMY_URL for testing database
SQL_ALCHEMY_URL = f'postgresql://{Settings.DB_USERNAME}:{Settings.DB_PASSWORD}@{Settings.DATABASE_HOSTNAME}:{Settings.DATABASE_PORT}/{Settings.DATABASE_NAME}_test'
engine = create_engine(SQL_ALCHEMY_URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestSessionLocal()
    try:
            yield db
    finally:
            db.close()

@pytest.fixture
def client(session):    
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    # code before we run our test (up)
    yield TestClient(app) # sync before code before tests are run (yield)
    # code after test are over (down)x


@pytest.fixture
def test_user(client):
    user_data = {"email": "hello123@gmail.com", "password": "password123"}
    res = client.post("/user/", json= user_data)
    assert res.status_code == 201

    # add password in new_user dictionary
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user