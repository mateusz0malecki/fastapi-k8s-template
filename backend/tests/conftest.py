import pytest
import json
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database, drop_database

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import create_app
from db.database import Base, get_db
from db.db_models.user_models import UserModel
from auth.jwt_helper import get_current_user
from settings import get_settings

app = create_app()
app_settings = get_settings()

SQLALCHEMY_DATABASE_URL = app_settings.test_db_url
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# USE THIS FOR SQLite:
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def db_engine():
    if not database_exists(SQLALCHEMY_DATABASE_URL):
        create_database(engine.url)
    Base.metadata.create_all(bind=engine)
    yield engine
    drop_database(SQLALCHEMY_DATABASE_URL)


@pytest.fixture(scope="module")
def db(db_engine):
    connection = db_engine.connect()
    connection.begin()
    db = SessionTesting(bind=connection)
    yield db
    db.rollback()
    connection.close()


@pytest.fixture(scope="module")
def client(db):
    app.dependency_overrides[get_db] = lambda: db

    async def avoid_token():
        user = UserModel.get_user_by_email(db, "email@email.com")
        if user:
            return user
        return UserModel(
            email="email@email.com",
            is_active=True,
            is_admin=True
        )

    app.dependency_overrides[get_current_user] = avoid_token
    with TestClient(app) as c:
        yield c


@pytest.fixture
def register_users(client):
    data_users = [
        {
            "email": "email@email.com",
            "password": "password123",
            "repeatPassword": "password123"
        },
        {
            "email": "test@test.com",
            "password": "password123",
            "repeatPassword": "password123"
        },
    ]
    [client.post(f'{app_settings.root_path}/register', json.dumps(data_user)) for data_user in data_users]
