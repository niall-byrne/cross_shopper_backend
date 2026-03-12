"""Test the 0006 items migration."""

from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

import pytest
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
    kwargs.setdefault(
        'brand',
        self.instance(
            "Brand",
            name=self.unique,
        ),
    )
    kwargs.setdefault(
        'packaging',
        self.instance(
            "Packaging",
            container=self.instance(
                "PackagingContainer",
                name=self.unique,
            ),
            unit=self.instance(
                "PackagingUnit",
                name=self.unique,
            ),
        ),
    )

    item: "models.Item" = self.instance(
        "Item",
        **kwargs,
    )
    return item


@pytest.mark.django_db
class TestItemsMigration009:

  @pytest.fixture(scope="function", autouse=True)
  def reset(self, migrator: "Migrator") -> "Generator[None, None, None]":
    yield
    migrator.reset()

  def test_migrate__single_item__creates_price_groups(
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
    old_item = old_models.item(price_group=None)

    new_state = migrator.apply_tested_migration(
        (
            'items',
            '0009_populate_item_price_group',
        )
    )
    new_models = ItemAppModelSet.create(new_state)
    new_item = new_models.Item.objects.get(pk=old_item.pk)

    assert new_item.price_group is not None
    assert new_item.price_group.is_non_gmo == new_item.is_non_gmo
    assert new_item.price_group.is_organic == new_item.is_organic
    assert new_item.price_group.name == new_item.name
    assert new_item.price_group.quantity == 100
    assert new_item.price_group.unit == new_item.packaging.unit

  def test_migrate__multi_item__share_price_groups(
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
    old_item1 = old_models.item(
        is_non_gmo=False,
        is_organic=False,
        price_group=None,
    )
    old_item2 = old_models.item(
        name=old_item1.name,
        is_non_gmo=False,
        is_organic=False,
        price_group=None,
        packaging=old_item1.packaging,
    )

    new_state = migrator.apply_tested_migration(
        (
            'items',
            '0009_populate_item_price_group',
        )
    )
    new_models = ItemAppModelSet.create(new_state)
    new_item1 = new_models.Item.objects.get(pk=old_item1.pk)
    new_item2 = new_models.Item.objects.get(pk=old_item2.pk)

    assert new_item1.price_group is not None
    assert new_item2.price_group is not None
    assert new_item1.price_group.pk == new_item2.price_group.pk
    assert new_item1.price_group.is_non_gmo == new_item1.is_non_gmo
    assert new_item1.price_group.is_organic == new_item1.is_organic
    assert new_item1.price_group.name == new_item1.name
    assert new_item1.price_group.quantity == 100
    assert new_item1.price_group.unit == new_item1.packaging.unit
