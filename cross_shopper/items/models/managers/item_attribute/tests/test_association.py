"""Test the Assocations model manager for the ItemAttribute model."""

from typing import TYPE_CHECKING

import pytest
from items.models import Attribute, ItemAttribute

if TYPE_CHECKING:  # no cover
  from django.db.models import QuerySet


@pytest.mark.django_db
class TestItemAttribute:

  def test_get_items__has_associated_items__returns_items(
      self,
      item_attribute_batch: "QuerySet[ItemAttribute]",
  ) -> None:
    attribute_ids = item_attribute_batch.values_list(
        "attribute__id",
        flat=True,
    )
    item_ids = item_attribute_batch.values_list(
        "item__id",
        flat=True,
    )
    attributes = Attribute.objects.filter(id__in=attribute_ids)

    qs = ItemAttribute.associations.get_items(attributes)

    assert list(qs.values_list("id", flat=True)) == list(item_ids)

  def test_get_items__no_associated_items__returns_empty_list(
      self,
      attribute_batch: "QuerySet[Attribute]",
  ) -> None:
    qs = ItemAttribute.associations.get_items(attribute_batch)

    assert list(qs) == []

  @pytest.mark.usefixtures("attribute")
  def test_with_items__returns_correct__attributes(
      self,
      item_attribute_batch: "QuerySet[ItemAttribute]",
  ) -> None:
    attribute_ids = item_attribute_batch.values_list(
        "attribute__id",
        flat=True,
    )
    attributes = Attribute.objects.filter(id__in=attribute_ids)

    qs = ItemAttribute.associations.with_items(Attribute.objects.all())

    assert list(qs) == list(attributes)

  @pytest.mark.usefixtures("item_attribute_batch")
  def test_with_no_items__returns_correct_attributes(
      self,
      attribute: "Attribute",
  ) -> None:
    qs = ItemAttribute.associations.with_no_items(Attribute.objects.all())

    assert list(qs) == list(Attribute.objects.filter(id=attribute.pk))
