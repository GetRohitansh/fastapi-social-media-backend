from fastapi.testclient import TestClient
from app.main import app
from app.config import Settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db, Base
from app.oauth2 import create_access_token
from app import models
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

@pytest.fixture
def test_user_2(client):
    user_data = {"email": "user123@gmail.com", "password": "123 password"}
    res = client.post("/user/", json= user_data)
    assert res.status_code == 201

    # add password in new_user dictionary
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


############################ create token for authentication ############################

@pytest.fixture
def token(test_user):
    return create_access_token({'user_id': test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client

############################ posts ############################

@pytest.fixture
def test_posts(test_user, session, test_user_2):
    posts_data = [{
        "title": "title 1",
        "content": "content 1",
        "owner_id": test_user['id']
    },{
        "title": "title 2",
        "content": "content 2",
        "owner_id": test_user['id']
    },{
        "title": "title 3",
        "content": "content 3",
        "owner_id": test_user['id']
    },{
        "title": "title 4",
        "content": "content 4",
        "owner_id": test_user_2['id']
    }]

    # Adding posts directly to database
    # so that we can test get post function
    def create_post_model(post):
        return models.Post(**post)
    
    post_map = map(create_post_model, posts_data)
    post_list = list(post_map)
    
    session.add_all(post_list)
    session.commit()

    posts = session.query(models.Post).all()
    return posts