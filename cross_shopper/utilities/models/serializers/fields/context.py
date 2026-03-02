"""A custom serializer field to extract values from the serializer context."""

from typing import TYPE_CHECKING

from rest_framework import serializers

if TYPE_CHECKING:  #no cover
  from typing import Any, Callable, Optional


class SerializerContextField(serializers.Field):
  """A custom field to extract values from the serializer context."""

  context_field: "str"
  default_value: "Optional[Callable[[], Any]]"

  class Messages:
    no_context_field = (
        "A serializer ContextField requires a value for "
        "context_field to be specified."
    )

  def __init__(
      self,
      *args: "Any",
      **kwargs: "Any",
  ) -> None:
    kwargs['source'] = '*'
    kwargs['read_only'] = True
    self.default_value = kwargs.pop("default_value", None)
    self.context_field = kwargs.pop("context_field", None)
    if (not self.context_field):
      raise Exception(self.Messages.no_context_field)
    super().__init__(*args, **kwargs)

  def _get_context_value(self) -> "Any":
    context_value = self.context.get(self.context_field, None)
    if not context_value and self.default_value is not None:
      context_value = self.default_value()

    return context_value

  def to_representation(self, value: "Any") -> "Any":
    """Transform the *outgoing* native value into primitive data."""
    return self._get_context_value()
