import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session

from backend.app import app
from backend.database import get_session
from backend.models import User, table_registry
from backend.security import get_password_hash


@pytest.fixture()
def token(client, user):
    response = client.post(
        '/auth/token',
        data={
            'username': user.email,
            'password': user.plain_password,
        }
    )

    cookies = response.cookies
    return cookies


@pytest.fixture()
def other_user(session):
    new_user = User(
        username='marcelo',
        email='marcelo@marcelo.com',
        password=get_password_hash('12345'),
    )

    session.add(new_user)
    session.commit()

    new_user.plain_password = '12345'
    return new_user


@pytest.fixture()
def user(session):
    new_user = User(
        username='joao',
        email='joao@joao.com',
        password=get_password_hash('12345'),
    )

    session.add(new_user)
    session.commit()

    new_user.plain_password = '12345'
    return new_user


@pytest.fixture()
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture()
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)
