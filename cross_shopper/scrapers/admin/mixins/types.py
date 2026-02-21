"""Type for the scrapers app admin model mixin classes."""

from typing import TYPE_CHECKING, Protocol, TypeVar, Union

if TYPE_CHECKING:  # no cover
  from django.db.models import Model
  from django.http import HttpRequest

ModelType = TypeVar("ModelType", bound="Model")


class AdminMixinType(Protocol):
  def message_user(  # noqa: D102
    self,
    request: "HttpRequest",
    message: str,
    level: Union[int, str] = ...,
    extra_tags: str = ...,
    fail_silently: bool = ...,
  ) -> None:
    ...
