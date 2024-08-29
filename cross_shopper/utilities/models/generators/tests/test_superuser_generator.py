"""Test the create_superuser function."""

import pytest
from django.db import Error
from utilities.models.generators.superuser import (
    ERROR_MESSAGE,
    create_superuser,
)


@pytest.mark.django_db
class TestCreateSuperUser:

  def test_create_defaults(self) -> None:
    user = create_superuser()

    assert user.get_username() == "admin"
    assert getattr(user, user.get_email_field_name()) == "test@example.com"
    assert user.check_password("admin")

  def test_create_default_twice(self) -> None:
    create_superuser()

    with pytest.raises(Error) as exc:
      create_superuser()

    assert str(exc.value) == ERROR_MESSAGE

  def test_create_specified(self) -> None:
    test_username = "superuser"
    test_password = "superuser"

    user = create_superuser(username=test_username, password=test_password)

    assert user.get_username() == test_username
    assert getattr(user, user.get_email_field_name()) == "test@example.com"
    assert user.check_password(test_password)
