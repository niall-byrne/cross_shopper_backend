"""Test the Assocations model manager for the PriceGroup model."""

from typing import TYPE_CHECKING

import pytest
from items.models import Attribute, PriceGroupAttribute

if TYPE_CHECKING:  # no cover
  from django.db.models import QuerySet


@pytest.mark.django_db
class TestPriceGroupAttribute:

  def test_get_price_groups__has_associated_pg__returns_items(
      self,
      price_group_attribute_batch: "QuerySet[PriceGroupAttribute]",
  ) -> None:
    attribute_ids = price_group_attribute_batch.values_list(
        "attribute__id",
        flat=True,
    )
    pg_ids = price_group_attribute_batch.values_list(
        "price_group__id",
        flat=True,
    )
    attributes = Attribute.objects.filter(id__in=attribute_ids)

    qs = PriceGroupAttribute.associations.get_price_groups(attributes)

    assert list(qs.values_list("id", flat=True)) == list(pg_ids)

  def test_get_price_groups__no_associated_pg__returns_empty_list(
      self,
      attribute_batch: "QuerySet[Attribute]",
  ) -> None:
    qs = PriceGroupAttribute.associations.get_price_groups(attribute_batch)

    assert list(qs) == []

  @pytest.mark.usefixtures("attribute")
  def test_with_price_groups__returns_correct__attributes(
      self,
      price_group_attribute_batch: "QuerySet[PriceGroupAttribute]",
  ) -> None:
    attribute_ids = price_group_attribute_batch.values_list(
        "attribute__id",
        flat=True,
    )
    attributes = Attribute.objects.filter(id__in=attribute_ids)

    qs = PriceGroupAttribute.associations.with_price_groups(
        Attribute.objects.all(),
    )

    assert list(qs) == list(attributes)

  @pytest.mark.usefixtures("price_group_attribute_batch")
  def test_with_no_items__returns_correct_attributes(
      self,
      attribute: "Attribute",
  ) -> None:
    qs = PriceGroupAttribute.associations.with_no_price_groups(
        Attribute.objects.all(),
    )

    assert list(qs) == list(Attribute.objects.filter(id=attribute.pk))
