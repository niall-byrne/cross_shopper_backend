"""Item data migration for attributes."""

import re
from typing import TYPE_CHECKING, cast

from django.core.exceptions import ObjectDoesNotExist
from django.db import migrations, transaction

if TYPE_CHECKING:
  from django.apps.registry import Apps
  from django.db.backends.base.schema import BaseDatabaseSchemaEditor
  from items.models import Attribute, Item


def forwards_func(
    apps: "Apps",
    schema_editor: "BaseDatabaseSchemaEditor",
) -> None:
  AttributeModel = cast("Attribute", apps.get_model("items", "Attribute"))
  ItemModel = cast("Item", apps.get_model("items", "Item"))

  legacy_description = re.compile(r"^.+(\((.+)\))$")

  with transaction.atomic():
    for item in ItemModel.objects.all():
      match = re.match(legacy_description, item.name)
      if match:
        name_replace_text = match.group(1)
        attribute_names = match.group(2).strip().split(",")
        item.name = item.name.replace(name_replace_text, "").strip()

        for attribute_name in attribute_names:
          attribute_name = attribute_name.strip()
          try:
            attribute = AttributeModel.objects.get(name__iexact=attribute_name)
          except ObjectDoesNotExist:
            attribute_name = attribute_name[0].upper() + attribute_name[1:]
            attribute = AttributeModel.objects.create(name=attribute_name)
          item.attribute.add(attribute)

      item.save()


def backwards_func(
    apps: "Apps",
    schema_editor: "BaseDatabaseSchemaEditor",
) -> None:
  AttributeModel = cast("Attribute", apps.get_model("items", "Attribute"))
  ItemModel = cast("Item", apps.get_model("items", "Item"))

  with transaction.atomic():
    for item in ItemModel.objects.all():
      attributes = list(
          item.attribute.all().order_by("name").values_list("name", flat=True)
      )

      if attributes:
        item.name = item.name + " ({})".format(", ".join(attributes))
        item.attribute.clear()
        item.save()

    AttributeModel.objects.all().delete()


class Migration(migrations.Migration):
  dependencies = [
      ("items", "0005_add_item_attribute"),
  ]

  operations = [
      migrations.RunPython(forwards_func, backwards_func),
  ]
