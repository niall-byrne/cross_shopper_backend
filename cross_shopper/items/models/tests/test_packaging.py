"""Test the Packaging model."""

import pytest
from django.core.exceptions import ValidationError
from items.models import Packaging, PackagingContainer, PackagingUnit


@pytest.mark.django_db
class TestPackaging:

  def test_constraint__unique_together(
      self,
      packaging_as_non_bulk: Packaging,
  ) -> None:
    packaging2 = Packaging(
        container=packaging_as_non_bulk.container,
        quantity=packaging_as_non_bulk.quantity,
        unit=packaging_as_non_bulk.unit,
    )

    with pytest.raises(ValidationError) as exc:
      packaging2.save()

    assert str(exc.value) == str(
        {
            "__all__":
                [
                    "Packaging with this Quantity, Container and Unit "
                    "already exists.",
                ]
        }
    )

  def test_clean__with_container__with_quantity__with_unit__no_exception(
      self,
      packaging_container: "PackagingContainer",
      packaging_unit: "PackagingUnit",
  ) -> None:
    quantity = 100

    packaging = Packaging(
        container=packaging_container,
        quantity=quantity,
        unit=packaging_unit,
    )
    packaging.save()

    assert packaging.container == packaging_container
    assert packaging.container is not None
    assert packaging.quantity == quantity
    assert packaging.quantity is not None
    assert packaging.unit == packaging_unit
    assert packaging.unit is not None

  @pytest.mark.parametrize("missing_field", ["container", "quantity"])
  def test_clean__vary_container__vary_quantity__with_unit__exception(
      self,
      packaging_container: "PackagingContainer",
      packaging_unit: "PackagingUnit",
      missing_field: str,
  ) -> None:
    quantity = 100

    with pytest.raises(ValidationError) as exc:
      packaging = Packaging(
          container=packaging_container,
          quantity=quantity,
          unit=packaging_unit,
      )
      setattr(packaging, missing_field, None)
      packaging.save()

    assert str(exc.value) == str({missing_field: ["This field is required."]})
    assert getattr(packaging, missing_field) is None

  def test_clean__no_container__no_quantity__with_unit__no_exception(
      self,
      packaging_unit: "PackagingUnit",
  ) -> None:
    packaging = Packaging(
        container=None,
        quantity=None,
        unit=packaging_unit,
    )

    assert packaging.container is None
    assert packaging.quantity is None
    assert packaging.unit == packaging_unit
    assert packaging.unit is not None

  def test_clean__no_container__no_quantity__no_unit__exception(self,) -> None:

    with pytest.raises(ValidationError) as exc:
      packaging = Packaging(
          container=None,
          quantity=None,
          unit=None,
      )
      packaging.save()

    assert str(exc.value) == str({"unit": ["This field cannot be null."]})

  def test_str__with_container__with_quantity__with_unit__correct_value(
      self,
      packaging_container: "PackagingContainer",
      packaging_unit: "PackagingUnit",
  ) -> None:
    packaging = Packaging(
        container=packaging_container,
        quantity=100,
        unit=packaging_unit,
    )

    assert str(packaging) == (
        f"{str(packaging.container)}: "
        f"{str(packaging.quantity)} {str(packaging.unit)}"
    )

  def test_str__no_container__no_quantity__with_unit__correct_value(
      self,
      packaging_unit: "PackagingUnit",
  ) -> None:
    packaging = Packaging(
        container=None,
        quantity=None,
        unit=packaging_unit,
    )

    assert str(packaging) == (
        f"{packaging.CONTAINER_NAME_FOR_BULK_PACKAGING} per "
        f"{str(packaging.unit)}"
    )
