"""Function for generating model admin list display column entries."""
from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Protocol,
    Sequence,
    TypeVar,
)

from django.contrib import admin
from . import ColumnLinkConfig, ColumnObjectConfig

if TYPE_CHECKING:
  from django.db.models import Model
  from django.utils.safestring import SafeString

T = TypeVar("T", bound="admin.ModelAdmin[Any]")

AliasColumnMethod = (
    Callable[[admin.ModelAdmin["Model"], "Model"], "SafeString | None"]
)

AliasColumnConfigType = ColumnLinkConfig | ColumnObjectConfig
AliasColumnType = AliasColumnConfigType | str
AliasConfiguration = Sequence[AliasColumnType]


class ColumnGenerator(Protocol):

  def __call__(  # noqa: D102
      self,
      model_admin: type[T],
  ) -> type[T]:
    ...
