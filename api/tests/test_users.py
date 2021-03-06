import pytest
from fastapi.testclient import TestClient
from ..database import Base, get_db
from .testing_database import engine, get_test_db, TestingSessionLocal
from ..main import app
from ..services import user_service
from sqlalchemy.orm import Session


testclient = TestClient(app)


def setup_function():
    app.dependency_overrides[get_db] = get_test_db
    Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="session")
def db():
    yield TestingSessionLocal()


@pytest.fixture
def user_register_dict() -> dict[str, str]:
    return {
        "username": "Janusz",
        "email": "janusz@abc.pl",
        "password1": "krowa123",
        "password2": "krowa123"
    }


@pytest.fixture
def user_login_dict() -> dict[str, str]:
    return {
        "username": "Janusz",
        "password": "krowa123"
    }


def test_register_user(user_register_dict: dict[str, str]):
    response = testclient.post("/auth/register", json=user_register_dict)
    assert response.ok
    assert response.json() == {'detail': 'Confirmation email sent'}


def test_cannot_login_without_confirmation(user_login_dict: dict[str, str]):
    response = testclient.post("/auth/login", json=user_login_dict)
    assert response.status_code == 401
    assert response.json() == {'detail': 'Unable to authenticate user'}


def test_user_login(user_login_dict: dict[str, str], db: Session):
    user = user_service.get_user(db=db, username=user_login_dict['username'])
    print(user)
