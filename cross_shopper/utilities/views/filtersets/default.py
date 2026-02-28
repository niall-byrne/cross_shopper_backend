"""View filterset that populates default values for query params."""

from typing import TYPE_CHECKING, Any

from django_filters import rest_framework as filters

if TYPE_CHECKING:  # no cover
  from typing import Any


class DefaultFilterSet(filters.FilterSet):
  """View filterset that populates default values for query params."""

  def __init__(self, *args: "Any", **kwargs: "Any") -> None:
    super().__init__(*args, **kwargs)
    self.data = self.data.copy()
    for filter_name, filter in self.filters.items():
      method = getattr(self, "default_" + filter_name, None)
      if method and filter_name not in self.data:
        self.data[filter_name] = method()
