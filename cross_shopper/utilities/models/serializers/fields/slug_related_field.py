"""A custom serializer field to create non-existent slug related models."""

from typing import TYPE_CHECKING

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from utilities.models.serializers.fields.mixins.peroxide import (
    PeroxideFieldMixin,
)

if TYPE_CHECKING:  # no cover
  from typing import Any

  from django.db.models import Model, QuerySet


class CreatableSlugRelatedField(
    serializers.SlugRelatedField["Model"],
    PeroxideFieldMixin,
):
  """A custom serializer field to create non-existent slug related models."""

  case_sensitive: bool
  case_sensitive_lookups = {True: "exact", False: "iexact"}
  slug_field: str
  queryset: "QuerySet[Model]"

  def __init__(
      self,
      *args: "Any",
      case_sensitive: "bool" = True,
      **kwargs: "Any",
  ) -> None:
    super().__init__(*args, **kwargs)
    self.case_sensitive = case_sensitive

  def to_internal_value(self, data: "str") -> "Model":
    """Sanitizes the data and then gets or creates the slug related model."""
    sanitized_data = self.sanitize(data)
    lookup = "{}__{}".format(
        self.slug_field,
        self.case_sensitive_lookups[self.case_sensitive],
    )
    try:
      return self.queryset.get(**{lookup: sanitized_data})
    except ObjectDoesNotExist:
      return self.queryset.create(**{self.slug_field: sanitized_data})
