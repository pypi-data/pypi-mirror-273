import pytest

from django.contrib.auth import get_user_model

from django_email_auth.backend import EmailOrUsernameBackend

UserModel = get_user_model()


@pytest.fixture
def user(db):
    return UserModel.objects.create_user(username="testuser", email="testuser@example.com", password="testpassword")


@pytest.fixture
def backend():
    return EmailOrUsernameBackend()


@pytest.mark.django_db
def test_authenticate_with_username(backend, user):
    assert backend.authenticate(None, username="testuser", password="testpassword") == user


@pytest.mark.django_db
def test_authenticate_with_email(backend, user):
    assert backend.authenticate(None, username="testuser@example.com", password="testpassword") == user


@pytest.mark.django_db
def test_authenticate_with_incorrect_username(backend):
    assert backend.authenticate(None, username="wronguser", password="testpassword") is None


@pytest.mark.django_db
def test_authenticate_with_incorrect_email(backend):
    assert backend.authenticate(None, username="wronguser@example.com", password="testpassword") is None
