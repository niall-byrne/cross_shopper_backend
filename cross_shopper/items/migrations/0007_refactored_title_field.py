"""PackagingContainer data migration for TitleField refactor."""
from __future__ import annotations

from typing import TYPE_CHECKING, cast

from django.db import migrations, transaction

if TYPE_CHECKING:
  from django.apps.registry import Apps
  from django.db.backends.base.schema import BaseDatabaseSchemaEditor
  from items.models import PackagingContainer


def save_all_func(
    apps: Apps,
    schema_editor: BaseDatabaseSchemaEditor,
) -> None:
  PackagingContainerModel = cast(
      "PackagingContainer",
      apps.get_model("items", "PackagingContainer"),
  )

  with transaction.atomic():
    for packaging_container in PackagingContainerModel.objects.all():
      packaging_container.save()


class Migration(migrations.Migration):

  dependencies = [
      ("items", "0006_populate_item_attribute"),
  ]

  operations = [
      migrations.RunPython(save_all_func, save_all_func),
  ]
