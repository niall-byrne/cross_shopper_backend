"""Test the 0006 items migration."""

from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

import pytest
from items import constants
from utilities.testing.migrations.app_model_set import AppModelSet

if TYPE_CHECKING:
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
  PriceGroup: "models.PriceGroup"

  module: ClassVar[str] = "items"

  def item(self, **kwargs: "Any") -> "models.Item":
    brand = self.instance("Brand", name=self.unique)
    packaging_container = self.instance(
        "PackagingContainer",
        name=self.unique,
    )
    packaging_unit = self.instance("PackagingUnit", name=self.unique)
    packaging = self.instance(
        "Packaging",
        container=packaging_container,
        unit=packaging_unit,
    )
    item: "models.Item" = self.instance(
        "Item",
        brand=brand,
        packaging=packaging,
        **kwargs,
    )
    return item


@pytest.mark.django_db
class TestItemsMigration009:

  @pytest.fixture(scope="function", autouse=True)
  def reset(self, migrator: "Migrator") -> "Generator[None, None, None]":
    yield
    migrator.reset()

  def test_migrate__single_item__not_organic__creates_price_groups(
      self,
      migrator: "Migrator",
  ) -> None:
    old_state = migrator.apply_initial_migration(
        (
            'items',
            '0008_add_item_price_group',
        )
    )
    old_models = ItemAppModelSet.create(old_state)
    old_item = old_models.item(is_organic=False, price_group=None)

    new_state = migrator.apply_tested_migration(
        (
            'items',
            '0009_populate_item_price_group',
        )
    )
    new_models = ItemAppModelSet.create(new_state)
    new_item = new_models.Item.objects.get(pk=old_item.pk)

    assert new_item.price_group.name == new_item.name
    assert new_item.price_group.quantity == 100
    assert new_item.price_group.unit == new_item.packaging.unit

  def test_migrate__multi_item__not_organic__share_price_groups(
      self,
      migrator: "Migrator",
  ) -> None:
    old_state = migrator.apply_initial_migration(
        (
            'items',
            '0008_add_item_price_group',
        )
    )
    old_models = ItemAppModelSet.create(old_state)
    old_item1 = old_models.item(is_organic=False, price_group=None)
    old_item2 = old_models.item(
        name=old_item1.name,
        is_organic=False,
        price_group=None,
    )
    old_item2.save()

    new_state = migrator.apply_tested_migration(
        (
            'items',
            '0009_populate_item_price_group',
        )
    )
    new_models = ItemAppModelSet.create(new_state)
    new_item1 = new_models.Item.objects.get(pk=old_item1.pk)
    new_item2 = new_models.Item.objects.get(pk=old_item2.pk)

    assert new_item1.price_group.pk == new_item2.price_group.pk
    assert new_item1.price_group.name == new_item1.name
    assert new_item1.price_group.quantity == 100
    assert new_item1.price_group.unit == new_item1.packaging.unit

  def test_migrate__single_item__is_organic__creates_price_groups(
      self,
      migrator: "Migrator",
  ) -> None:
    old_state = migrator.apply_initial_migration(
        (
            'items',
            '0008_add_item_price_group',
        )
    )
    old_models = ItemAppModelSet.create(old_state)
    old_item = old_models.item(is_organic=True, price_group=None)

    new_state = migrator.apply_tested_migration(
        (
            'items',
            '0009_populate_item_price_group',
        )
    )
    new_models = ItemAppModelSet.create(new_state)
    new_item = new_models.Item.objects.get(pk=old_item.pk)

    assert new_item.price_group.name == (
        f"{constants.ITEM_NAME_PREFIX_ORGANIC} {new_item.name}"
    )
    assert new_item.price_group.quantity == 100
    assert new_item.price_group.unit == new_item.packaging.unit

  def test_migrate__multi_item__is_organic__share_price_groups(
      self,
      migrator: "Migrator",
  ) -> None:
    old_state = migrator.apply_initial_migration(
        (
            'items',
            '0008_add_item_price_group',
        )
    )
    old_models = ItemAppModelSet.create(old_state)
    old_item1 = old_models.item(is_organic=True, price_group=None)
    old_item2 = old_models.item(
        name=old_item1.name,
        is_organic=True,
        price_group=None,
    )
    old_item2.save()

    new_state = migrator.apply_tested_migration(
        (
            'items',
            '0009_populate_item_price_group',
        )
    )
    new_models = ItemAppModelSet.create(new_state)
    new_item1 = new_models.Item.objects.get(pk=old_item1.pk)
    new_item2 = new_models.Item.objects.get(pk=old_item2.pk)

    assert new_item1.price_group.pk == new_item2.price_group.pk
    assert new_item1.price_group.name == (
        f"{constants.ITEM_NAME_PREFIX_ORGANIC} {new_item1.name}"
    )
    assert new_item1.price_group.quantity == 100
    assert new_item1.price_group.unit == new_item1.packaging.unit
