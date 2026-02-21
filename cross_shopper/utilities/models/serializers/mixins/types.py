"""Type for the utilities model serializer mixin classes."""

from typing import TYPE_CHECKING, Any, Dict, Protocol, TypeVar

if TYPE_CHECKING:  # no cover
  from django.db.models import Model

ModelType = TypeVar('ModelType', bound='Model')


class SerializerMixinType(Protocol):
  context: Dict[str, Any]
