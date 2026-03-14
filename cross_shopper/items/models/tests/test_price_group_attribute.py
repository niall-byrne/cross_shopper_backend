"""Test the PriceGroupAttribute model."""

import pytest
from django.core.exceptions import ValidationError
from items.models import PriceGroupAttribute


@pytest.mark.django_db
class TestPriceGroupAttribute:

  def test_constraint__unique_together(
      self,
      price_group_attribute: PriceGroupAttribute,
  ) -> None:
    price_group_attribute2 = PriceGroupAttribute(
        price_group=price_group_attribute.price_group,
        attribute=price_group_attribute.attribute,
    )

    with pytest.raises(ValidationError) as exc:
      price_group_attribute2.save()

    assert str(exc.value) == str(
        {
            '__all__':
                [
                    'Price group attribute with this Price group and Attribute '
                    'already exists.'
                ],
        }
    )

  def test_str__returns_str_of_scraper_config(
      self,
      price_group_attribute: PriceGroupAttribute,
  ) -> None:
    assert str(price_group_attribute) == (
        f"{price_group_attribute.price_group.name} - "
        f"{price_group_attribute.attribute}"
    )
