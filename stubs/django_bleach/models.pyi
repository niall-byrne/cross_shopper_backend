"""Type hints for django_bleach models."""

from typing import TypeVar

from django.db.models import CharField

_ST = TypeVar("_ST")
_GT = TypeVar("_GT")


class BleachField(CharField[_ST, _GT]):
  ...
