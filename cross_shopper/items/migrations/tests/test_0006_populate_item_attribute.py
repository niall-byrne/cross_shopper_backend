"""Test the 0006 items migration."""

from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

import pytest
from utilities.testing.migrations.app_model_set import AppModelSet

if TYPE_CHECKING:  # no cover
  from typing import Any, Generator

  from django_test_migrations.migrator import Migrator
  from items import models


@dataclass
class ItemAppModelSet(AppModelSet):
  Attribute: "models.Attribute"
  Brand: "models.Brand"
  Item: "models.Item"
  Packaging: "models.Packaging"
  PackagingContainer: "models.PackagingContainer"
  PackagingUnit: "models.PackagingUnit"

  module: ClassVar[str] = "items"

  def item(self, **kwargs: "Any") -> "models.Item":
    brand_old = self.instance("Brand", name=self.unique)
    packaging_container_old = self.instance(
        "PackagingContainer",
        name=self.unique,
    )
    packaging_unit_old = self.instance("PackagingUnit", name=self.unique)
    packaging_old = self.instance(
        "Packaging",
        container=packaging_container_old,
        unit=packaging_unit_old,
    )
    item: "models.Item" = self.instance(
        "Item",
        brand=brand_old,
        packaging=packaging_old,
        **kwargs,
    )
    return item


@pytest.mark.django_db
class TestItemsMigration006:

  @pytest.fixture(scope="function", autouse=True)
  def reset(self, migrator: "Migrator") -> "Generator[None, None, None]":
    yield
    migrator.reset()

  def test_migrate__no_brackets__no_attributes_created(
      self,
      migrator: "Migrator",
  ) -> None:
    old_state = migrator.apply_initial_migration(
        (
            "items",
            "0005_add_item_attribute",
        )
    )
    old_models = ItemAppModelSet.create(old_state)

    old_item = old_models.item(name="No Brackets")

    new_state = migrator.apply_tested_migration(
        (
            "items",
            "0006_populate_item_attribute",
        )
    )
    new_models = ItemAppModelSet.create(new_state)

    new_item = new_models.Item.objects.get(pk=old_item.pk)

    assert new_item.name == old_item.name
    assert new_item.attribute.all().count() == 0
    assert new_models.Attribute.objects.all().count() == 0

  def test_migrate__single_bracket__creates_capitalized_attributes(
      self,
      migrator: "Migrator",
  ) -> None:
    old_state = migrator.apply_initial_migration(
        (
            "items",
            "0005_add_item_attribute",
        )
    )
    old_models = ItemAppModelSet.create(old_state)

    old_item = old_models.item(name="Item (Value1, value2)")

    new_state = migrator.apply_tested_migration(
        (
            "items",
            "0006_populate_item_attribute",
        )
    )
    new_models = ItemAppModelSet.create(new_state)

    new_item = new_models.Item.objects.get(pk=old_item.pk)

    assert new_item.name == old_item.name.split(" ")[0]
    assert new_item.attribute.all().count() == 2
    assert new_item.attribute.all()[0].name == "Value1"
    assert new_item.attribute.all()[1].name == "Value2"

  def test_migrate__dual_brackets__creates_reused_capitalized_attributes(
      self,
      migrator: "Migrator",
  ) -> None:
    old_state = migrator.apply_initial_migration(
        (
            "items",
            "0005_add_item_attribute",
        )
    )
    old_models = ItemAppModelSet.create(old_state)

    old_item1 = old_models.item(name="Item1 (Value1, value2)")
    old_item2 = old_models.item(name="Item2 (Value1, value2)")

    new_state = migrator.apply_tested_migration(
        (
            "items",
            "0006_populate_item_attribute",
        )
    )
    new_models = ItemAppModelSet.create(new_state)

    new_item1 = new_models.Item.objects.get(pk=old_item1.pk)
    new_item2 = new_models.Item.objects.get(pk=old_item2.pk)

    for new, old in zip([new_item1, new_item2], [old_item1, old_item2]):
      assert new.name == old.name.split(" ")[0]
      assert new.attribute.all().count() == 2
      assert new.attribute.all()[0].name == "Value1"
      assert new.attribute.all()[1].name == "Value2"

    assert new_models.Attribute.objects.all().count() == 2

  def test_reverse__no_attributes__no_brackets_created(
      self,
      migrator: "Migrator",
  ) -> None:
    old_state = migrator.apply_initial_migration(
        (
            "items",
            "0006_populate_item_attribute",
        )
    )
    old_models = ItemAppModelSet.create(old_state)

    old_item = old_models.item(name="No Brackets")

    new_state = migrator.apply_tested_migration(
        (
            "items",
            "0005_add_item_attribute",
        )
    )
    new_models = ItemAppModelSet.create(new_state)

    new_item = new_models.Item.objects.get(pk=old_item.pk)

    assert new_item.name == old_item.name
    assert new_item.attribute.all().count() == 0
    assert new_models.Attribute.objects.all().count() == 0

  def test_migrate__single_attribute__creates_brackets(
      self,
      migrator: "Migrator",
  ) -> None:
    old_state = migrator.apply_initial_migration(
        (
            "items",
            "0006_populate_item_attribute",
        )
    )
    old_models = ItemAppModelSet.create(old_state)

    old_attribute = old_models.instance("Attribute", name=old_models.unique)
    old_item = old_models.item(name="Item")
    old_item.attribute.set([old_attribute])

    new_state = migrator.apply_tested_migration(
        (
            "items",
            "0005_add_item_attribute",
        )
    )
    new_models = ItemAppModelSet.create(new_state)

    new_item = new_models.Item.objects.get(pk=old_item.pk)

    assert new_item.name == old_item.name + f" ({old_attribute.name})"

  def test_migrate__dual_attributes__creates_brackets(
      self,
      migrator: "Migrator",
  ) -> None:
    old_state = migrator.apply_initial_migration(
        (
            "items",
            "0006_populate_item_attribute",
        )
    )
    old_models = ItemAppModelSet.create(old_state)

    old_attribute1 = old_models.instance("Attribute", name=old_models.unique)
    old_attribute2 = old_models.instance("Attribute", name=old_models.unique)
    old_item = old_models.item(name="Item",)
    old_item.attribute.set([old_attribute1, old_attribute2])

    new_state = migrator.apply_tested_migration(
        (
            "items",
            "0005_add_item_attribute",
        )
    )
    new_models = ItemAppModelSet.create(new_state)

    new_item = new_models.Item.objects.get(pk=old_item.pk)

    assert new_item.name == (
        old_item.name + f" ({old_attribute1.name}, {old_attribute2.name})"
    )
