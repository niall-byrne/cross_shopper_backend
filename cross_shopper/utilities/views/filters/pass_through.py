"""A filter that passes values to the request without touching queries."""

from typing import TYPE_CHECKING, Any

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
    self.model = for_model
    super().__init__(*args, **kwargs)

  def filter(self, qs: "QuerySet[Model]", value: "Any"):
    """Pass through the queryset but attach the param value to the request."""
    request = self.get_request()
    request.GET = request.GET.copy()
    request.GET.update({self.field_name: value})
    return qs

  def label(self):  # no cover
    """Ensure the label method is called with the correct model."""
    return super().label()
