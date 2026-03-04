"""A filter that passes values to the request without touching queries."""

from typing import TYPE_CHECKING

from django_filters.filters import QuerySetRequestMixin
from django_filters.rest_framework import CharFilter

if TYPE_CHECKING:  # no cover
  from typing import Any, Optional, Type

  from django.db.models import Model, QuerySet


class PassThroughFilter(CharFilter, QuerySetRequestMixin):
  """A filter that passes values to the request without touching queries."""

  def __init__(
      self,
      *args: "Any",
      for_model: "Optional[Type[Model]]" = None,
      **kwargs: "Any",
  ) -> None:
    self.for_model = for_model
    super().__init__(*args, **kwargs)

  def filter(self, qs: "QuerySet[Model]", value: "Any") -> "QuerySet[Model]":
    """Pass through the queryset but attach the param value to the request."""
    request = self.get_request()
    setattr(request, "GET", request.GET.copy())
    request.GET.update({self.field_name: value})
    return qs

  @property
  def label(self) -> "Any":
    """Override the base getter to ensure model data is populated."""
    if self.for_model is not None:
      setattr(self, "model", self.for_model)
    return super(
        CharFilter,
        PassThroughFilter,
    ).label.fget(self)  # type: ignore[attr-defined]

  @label.setter
  def label(self, value: "Any") -> None:
    """Override the base setter to ensure model data is populated."""
    self._label = value
