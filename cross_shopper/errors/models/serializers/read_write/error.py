"""Serializer to retrieve, list, create or update Errors."""

from typing import Any, Dict, List, cast

from errors.models import Error, ErrorType
from rest_framework import request, serializers, validators


class ErrorSerializerRW(serializers.ModelSerializer):
  """Serializer to retrieve, list, create or update Errors."""

  type = serializers.SlugRelatedField(
      queryset=ErrorType.objects.all(),
      slug_field="name",
  )
  count = serializers.HiddenField(default=1)

  class Meta:
    model = Error
    fields = (
        "id",
        "type",
        "item",
        "is_reoccurring",
        "scraper_config",
        "store",
        "count",
    )

  def get_unique_together_validators(
      self,
  ) -> List[validators.UniqueTogetherValidator]:
    """Disable unique together checks to enable update operations."""
    return []

  def update(self, instance: Error, validated_data: Dict[str, Any]) -> Error:
    """Update an existing instance."""
    api_request: request.Request = cast(
        request.Request,
        self.context.get('request'),
    )

    if api_request.method == "POST":
      validated_data["count"] = instance.count + 1

    return super().update(instance, validated_data)
