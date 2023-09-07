from fastapi.testclient import TestClient
from app.main import app
from app import schemas
from app.config import Settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db, Base
import pytest


# SQL_ALCHEMY_URL for testing database
SQL_ALCHEMY_URL = f'postgresql://{Settings.DB_USERNAME}:{Settings.DB_PASSWORD}@{Settings.DATABASE_HOSTNAME}:{Settings.DATABASE_PORT}/{Settings.DATABASE_NAME}_test'

engine = create_engine(SQL_ALCHEMY_URL)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency
# Whenever we get request through API we get connection/session to database which is closed after request is compeleted

# We change get_db to override_get_db for testing purpose whenever we test routes
def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    # code before we run our test (up)
    yield TestClient(app) # sync before code before tests are run (yield)
    # code after test are over (down)

def test_root(client):
    res = client.get("/")
    print(res.json().get('message'))
    assert res.json().get('message') == 'Hello World'
    assert res.status_code == 200

def test_create_user(client):
    res = client.post("/user/", json= {"email": "hello123@gmail.com", "password": "password123"})
    new_user = schemas.UserOut(**res.json())
    # print(res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201


