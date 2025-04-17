"""Test the PricingSerializer class."""

import decimal
from typing import TYPE_CHECKING, Dict, Union

import pytest
from django.core.exceptions import ValidationError
from pricing.models import Price
from pricing.models.defaults import default_pricing_week, default_pricing_year
from rest_framework.exceptions import \
    ValidationError as SerializerValidationError
from ..pricing import PricingSerializer

if TYPE_CHECKING:  # no cover
  from items.models import Item
  from stores.models import Store


@pytest.mark.django_db
class TestPricingSerializer:
  """Test the PricingSerializer class."""

  def test_serialization__correct_representation(
      self,
      price: "Price",
  ) -> None:
    serialized = PricingSerializer(price)

    assert serialized.data == {
        'id': price.pk,
        'amount': str(price.amount),
        'item': price.item.pk,
        'store': price.store.pk,
        'week': price.week,
        'year': price.year,
    }

  def test_deserialization__valid_input__non_existent__correct_model(
      self,
      item: "Item",
      store: "Store",
  ) -> None:
    pricing_data: Dict[str, Union[str, int]] = {
        'amount': '1000.01',
        'item': item.pk,
        'store': store.pk,
    }

    serialized = PricingSerializer(data=pricing_data)
    serialized.is_valid(raise_exception=True)
    instance = serialized.save()

    assert instance.amount == decimal.Decimal(pricing_data['amount'])
    assert instance.item == item
    assert instance.store == store
    assert instance.week == default_pricing_week.default_pricing_week()
    assert instance.year == default_pricing_year.default_pricing_year()

  def test_deserialization__valid_input__existent__database_error_only(
      self,
      item: "Item",
      store: "Store",
  ) -> None:
    duplicate_pricing_data: Dict[str, Union[str, int]] = {
        'amount': '1000.01',
        'item': item.pk,
        'store': store.pk,
    }
    instance = Price(
        amount=duplicate_pricing_data['amount'],
        item=item,
        store=store,
    )
    instance.save()

    serialized = PricingSerializer(data=duplicate_pricing_data)
    serialized.is_valid(raise_exception=True)

    with pytest.raises(ValidationError) as exc:
      serialized.save()

    assert exc.type != SerializerValidationError
