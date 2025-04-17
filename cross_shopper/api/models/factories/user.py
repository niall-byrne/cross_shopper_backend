"""Model factories for the API app."""
from __future__ import annotations

from typing import TYPE_CHECKING

import factory
from django.contrib.auth import get_user_model

if TYPE_CHECKING:
  from django.contrib.auth.base_user import AbstractBaseUser  # noqa: F401
  from .typing import AliasFaker

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory["AbstractBaseUser"]):
  first_name: AliasFaker[str] = factory.Faker("first_name")
  last_name: AliasFaker[str] = factory.Faker("last_name")
  password: AliasFaker[str] = factory.Faker("password")
  username: factory.Sequence[str] = factory.Sequence(lambda n: "User-%03d" % n)
  is_superuser = False

  class Meta:
    model = User
