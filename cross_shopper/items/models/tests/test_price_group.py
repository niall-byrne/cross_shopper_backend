"""Test the PriceGroup model."""

from typing import TYPE_CHECKING

import pytest
from django.core.exceptions import ValidationError
from items import constants
from items.models import PackagingUnit
from items.models.price_group import (
    PriceGroup,
)
from items.models.validators.price_group import PriceGroupMemberValidator

if TYPE_CHECKING:  # no cover
  from typing import Any, Callable, Dict

  from items.models import Attribute
  from items.models.factories.item import ItemWithPriceGroup


@pytest.mark.django_db
class TestPriceGroup:

  attribute_order_scenario = pytest.mark.parametrize(
      "attribute_count,summary_builder",
      (
          (0, lambda price_group: ''),
          (
              1, lambda price_group: '[{}]'.
              format(str(price_group.attribute.all()[0]))
          ),
          (
              2, lambda price_group: '[{}]'.format(
                  ", ".join(map(str, price_group.attribute.order_by('name')))
              )
          ),
      ),
  )

  def test_constraint__unique_together(
      self,
      price_group: "PriceGroup",
  ) -> None:
    price_group2 = PriceGroup(
        is_non_gmo=price_group.is_non_gmo,
        is_organic=price_group.is_organic,
        name=price_group.name,
        quantity=price_group.quantity,
        unit=price_group.unit,
    )

    with pytest.raises(ValidationError) as exc:
      price_group2.save()

    assert str(exc.value) == str(
        {
            '__all__':
                [
                    'Price group with this Name, Is non gmo, Is organic, '
                    'Quantity and Unit already exists.',
                ]
        }
    )

  @pytest.mark.parametrize("non_gmo", [True, False])
  def test_clean__is_organic__always_sets_non_gmo_to_true(
      self,
      price_group: "PriceGroup",
      non_gmo: bool,
  ) -> None:
    price_group.is_organic = True
    price_group.is_non_gmo = non_gmo

    price_group.save()

    assert price_group.is_non_gmo is True

  def test_clean__non_gmo_certification_incompatible__raises_exception(
      self,
      item_not_organic: "ItemWithPriceGroup",
  ) -> None:
    item_not_organic.price_group.is_non_gmo = not item_not_organic.is_non_gmo

    with pytest.raises(ValidationError) as exc:
      item_not_organic.price_group.save()

    assert str(exc.value) == str(
        {
            'is_non_gmo':
                [
                    PriceGroupMemberValidator.error_message.format(
                        **{
                            "item_attribute": "non-gmo certification",
                            "price_group_attribute": "non-gmo certification",
                        }
                    )
                ]
        }
    )

  def test_clean__organic_certification_incompatible__raises_exception(
      self,
      item_organic: "ItemWithPriceGroup",
  ) -> None:
    item_organic.price_group.is_organic = not item_organic.is_organic

    with pytest.raises(ValidationError) as exc:
      item_organic.price_group.save()

    assert str(exc.value) == str(
        {
            'is_organic':
                [
                    PriceGroupMemberValidator.error_message.format(
                        **{
                            "item_attribute": "organic certification",
                            "price_group_attribute": "organic certification",
                        }
                    )
                ]
        }
    )

  def test_clean__comparison_unit_incompatible__raises_exception(
      self,
      item: "ItemWithPriceGroup",
  ) -> None:
    incompatible_packaging_unit = PackagingUnit.objects.create(
        name="incompatible",
    )
    item.price_group.unit = incompatible_packaging_unit

    with pytest.raises(ValidationError) as exc:
      item.price_group.save()

    assert str(exc.value) == str(
        {
            'unit':
                [
                    PriceGroupMemberValidator.error_message.format(
                        **{
                            "item_attribute": "packaging unit",
                            "price_group_attribute": "comparison unit",
                        }
                    )
                ]
        }
    )

  @attribute_order_scenario
  def test_attribute_summary__vary_sorted_attributes__returns_correct_summary(
      self,
      price_group: "PriceGroup",
      attribute_alternate: "Attribute",
      attribute_count: int,
      summary_builder: "Callable[[PriceGroup], str]",
  ) -> None:
    if attribute_count == 0:
      price_group.attribute.clear()
    if attribute_count == 2:
      price_group.attribute.add(attribute_alternate)

      assert price_group.attribute_summary == summary_builder(price_group)

  @attribute_order_scenario
  def test_attribute_summary__vary_unsorted_attributes__returns_correct_summary(
      self,
      price_group: "PriceGroup",
      attribute_alternate: "Attribute",
      attribute_count: int,
      summary_builder: "Callable[[PriceGroup], str]",
  ) -> None:
    if attribute_count == 0:
      price_group.attribute.clear()
    if attribute_count == 2:
      price_group.attribute.add(attribute_alternate)
    price_group.attribute.set(price_group.attribute.all().reverse())

    assert price_group.attribute_summary == summary_builder(price_group)

  def test_has_item__no_related_item__returns_false(
      self,
      price_group: "PriceGroup",
  ) -> None:
    assert price_group.has_item is False

  def test_has_item__with_related_item__returns_true(
      self,
      item: "ItemWithPriceGroup",
  ) -> None:
    assert item.price_group.has_item is True

  def test_items__no_related_item___returns_empty_query_set(
      self,
      price_group: "PriceGroup",
  ) -> None:
    assert price_group.items.count() == 0

  def test_items__with_related_item__returns_set_of_items(
      self,
      item: "ItemWithPriceGroup",
  ) -> None:
    assert list(item.price_group.items) == [item]

  @pytest.mark.parametrize(
      'has_attributes,name_builder', (
          (
              False,
              lambda price_group: price_group.name,
          ),
          (
              True,
              lambda price_group: " ".
              join([
                  price_group.name,
                  price_group.attribute_summary,
              ]),
          ),
      )
  )
  def test_name_attributed__vary_attributes__returns_correct_name(
      self,
      price_group: "PriceGroup",
      has_attributes: "bool",
      name_builder: "Callable[[PriceGroup], str]",
  ) -> None:
    if not has_attributes:
      price_group.attribute.clear()

    assert price_group.name_attributed == name_builder(price_group)

  @pytest.mark.parametrize(
      "quantity,measure_template",
      (
          (1, "{single_measure}"),
          (100, "{multi_measure}"),
      ),
  )
  @pytest.mark.parametrize(
      "scenario", (
          {
              "is_non_gmo": False,
              "is_organic": False,
              "expected_template": "{name} per {measure}"
          },
          {
              "is_non_gmo": True,
              "is_organic": False,
              "expected_template": "{non_gmo} {name} per {measure}"
          },
          {
              "is_non_gmo": False,
              "is_organic": True,
              "expected_template": "{organic} {name} per {measure}"
          },
          {
              "is_non_gmo": True,
              "is_organic": True,
              "expected_template": "{organic} {name} per {measure}"
          },
      )
  )
  def test_name_full__vary_certifications__returns_correct_group_name(
      self,
      price_group: "PriceGroup",
      quantity: "int",
      measure_template: "str",
      scenario: "Dict[str, Any]",
  ) -> None:
    price_group.quantity = quantity
    price_group.is_non_gmo = scenario["is_non_gmo"]
    price_group.is_organic = scenario["is_organic"]

    assert str(price_group.name_full) == scenario['expected_template'].format(
        name=price_group.name_attributed,
        non_gmo=constants.ITEM_NAME_PREFIX_NON_GMO,
        organic=constants.ITEM_NAME_PREFIX_ORGANIC,
        single_measure={price_group.unit},
        measure=measure_template.format(
            single_measure=f"{price_group.unit}",
            multi_measure=f"{price_group.quantity}{price_group.unit}",
        )
    )

  @pytest.mark.parametrize("quantity", [1, 100])
  @pytest.mark.parametrize("non_gmo", [True, False])
  @pytest.mark.parametrize("is_organic", [True, False])
  def test_str__is_not_organic__returns_name_full(
      self,
      quantity: "int",
      price_group: "PriceGroup",
      non_gmo: bool,
      is_organic: bool,
  ) -> None:
    price_group.quantity = quantity
    price_group.is_organic = is_organic
    price_group.is_non_gmo = non_gmo

    assert str(price_group) == price_group.name_full
