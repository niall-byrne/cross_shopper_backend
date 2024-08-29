"""Generate a Django superuser."""
from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model
from django.db import Error

if TYPE_CHECKING:
  from django.contrib.auth.models import AbstractBaseUser

ERROR_MESSAGE = "The admin user already exists."


def create_superuser(
    username: str = "admin",
    password: str = "admin",
) -> AbstractBaseUser:
  """Create a django superuser, with the specified name and password."""
  User = get_user_model()

  exists = User.objects.all().filter(username=username).count()
  if exists:
    raise Error(ERROR_MESSAGE)  # pylint: disable=broad-exception-raised

  user = User(
      username=username,
      email="test@example.com",
      is_superuser=True,
      is_staff=True,
  )
  user.set_password(password)
  user.save()

  return user
