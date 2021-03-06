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


@pytest.fixture(scope="session")
def user_register_dict() -> dict[str, str]:
    return {
        "username": "Janusz",
        "email": "janusz@abc.pl",
        "password1": "krowa123",
        "password2": "krowa123"
    }


@pytest.fixture(scope="session")
def user_login_dict() -> dict[str, str]:
    return {
        "username": "Janusz",
        "password": "krowa123"
    }


@pytest.fixture(scope="session")
def token(user_login_dict) -> str:
    return user_service.generate_access_token({'sub': user_login_dict['username']})


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
    user.email.is_confirmed = True
    db.commit()
    response = testclient.post("/auth/login", json=user_login_dict)
    assert response.ok


def test_user_change_password(user_login_dict: dict[str, str], token: str):
    old_password = user_login_dict['password']
    new_password1 = "aaaaaaaaaa"
    new_password2 = new_password1
    bad_new_password = "bbbbbbbbb"
    data = {
        "old_password": old_password,
        "new_password1": new_password1,
        "new_password2": bad_new_password
    }
    headers = {"Authorization": f"Bearer {token}"}
    bad_response = testclient.post("/auth/change-password", json=data, headers=headers)
    assert bad_response.status_code == 422
    data.update(new_password2=new_password2)
    response = testclient.post("/auth/change-password", json=data, headers=headers)
    assert response.ok
