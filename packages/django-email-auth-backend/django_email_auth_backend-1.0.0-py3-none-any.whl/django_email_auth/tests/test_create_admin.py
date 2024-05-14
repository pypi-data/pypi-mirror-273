import pytest
import string
from django.core.management import CommandError
from django.contrib.auth.models import User

from django_email_auth.management.commands.create_admin import Command, generate_random_password


@pytest.mark.django_db
@pytest.mark.parametrize("username,email,password,auto,expected_error", [
    # Happy path tests
    ("admin", "admin@example.com", "securepassword123!", False, None),
    ("admin_auto", "autoadmin@example.com", None, True, None),
    # Edge cases
    ("", "", "", False, CommandError),
    # Error cases
    (None, "admin@example.com", "securepassword123!", False, CommandError),
    ("admin", None, "securepassword123!", False, CommandError),
    ("admin", "admin@example.com", None, False, None),
], ids=[
    "happy-path-provided-password",
    "happy-path-auto",
    "edge-case-empty-fields",
    "error-case-no-username",
    "error-case-no-email",
    "error-case-no-password",
])
def test_create_admin_command(username, email, password, auto, expected_error, settings):
    # Arrange
    settings.ADMINS=[
        ("admin_auto", "adminauto@example.com"),
    ]
    command = Command()
    options = {
        "username": username,
        "email": email,
        "password": password,
        "auto": auto,
        "database": "default",
        "verbosity": 0,
    }

    # Act and Assert
    if expected_error:
        with pytest.raises(expected_error):
            command.handle(**options)
    else:
        command.handle(**options)
        user_exists = User.objects.filter(username=username).exists()
        assert user_exists, f"User {username} should have been created"


@pytest.mark.parametrize("length,contains_digit,contains_punct", [
    (16, True, True),
], ids=[
    "password-length-and-complexity",
])
def test_generate_random_password(length, contains_digit, contains_punct):
    # Act
    password = generate_random_password()

    # Assert
    assert len(password) == length, \
        "Password length does not match expected"
    assert any(char.isdigit() for char in password) == contains_digit, \
        "Password does not contain a digit"
    assert any(char in string.punctuation for char in password) == contains_punct, \
        "Password does not contain a punctuation"
