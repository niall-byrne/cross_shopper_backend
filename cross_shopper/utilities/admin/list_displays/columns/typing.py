"""Function for generating model admin list display column entries."""

from typing import TYPE_CHECKING, Callable, Protocol, Sequence, TypeVar, Union

from django.contrib import admin
from . import ColumnLinkConfig, ColumnObjectConfig

if TYPE_CHECKING:  # no cover
  from typing import Any, Optional, Type

  from django.db.models import Model
  from django.utils.safestring import SafeString

T = TypeVar('T', bound="admin.ModelAdmin[Any]")

AliasColumnMethod = (
    Callable[[admin.ModelAdmin["Model"], "Model"], "Optional[SafeString]"]
)

AliasColumnConfigType = Union[ColumnLinkConfig, ColumnObjectConfig]
AliasColumnType = Union[str, AliasColumnConfigType]
AliasConfiguration = Sequence[AliasColumnType]


class ColumnGenerator(Protocol):

  def __call__(  # noqa: D102
      self,
      model_admin: "Type[T]",
  ) -> "Type[T]":
    ...
