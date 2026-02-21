"""Factories for ErrorType model instances."""

from typing import TYPE_CHECKING

import factory

if TYPE_CHECKING:  # no cover
  from errors.models import ErrorType  # noqa: F401


class ErrorTypeFactory(factory.django.DjangoModelFactory["ErrorType"]):
  name: "factory.Sequence[str]" = factory.Sequence(lambda n: "Type %03d" % n)

  class Meta:
    model = "errors.ErrorType"
