"""A boolean query parameter mixin for serializer classes."""

from typing import Optional, cast

from .types import SerializerMixinType


class BooleanQueryParamMixin:
  """A serializer mixin that provides boolean query param filtering."""

  def _as_mixin(self) -> "SerializerMixinType":
    return cast(SerializerMixinType, self)

  def get_boolean_query_param(self, query_param: str) -> Optional[bool]:
    """Check the specified query param for a boolean value."""
    request = self._as_mixin().context.get('request')
    boolean_mapping = {
        "true": True,
        "false": False,
    }

    if request:
      boolean_filter = request.query_params.get(query_param, None)
      if isinstance(boolean_filter, str) and boolean_filter in boolean_mapping:
        return boolean_mapping[boolean_filter.lower()]

    return None
