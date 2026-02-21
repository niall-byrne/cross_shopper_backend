"""Type for the scrapers app admin model mixin classes."""
from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, TypeVar

if TYPE_CHECKING:
  from django.db.models import Model
  from django.http import HttpRequest

ModelType = TypeVar("ModelType", bound="Model")


class AdminMixinType(Protocol):

  def message_user( # noqa: D102
      self,
      request: HttpRequest,
      message: str,
      level: int | str = ...,
      extra_tags: str = ...,
      fail_silently: bool = ...,
  ) -> None:
    ...
