"""Test the PackagingUnit model."""

import pytest
from django.core.exceptions import ValidationError
from items.models.packaging_unit import CONSTRAINT_NAMES, PackagingUnit


@pytest.mark.django_db
class TestPackagingUnit:

  mocked_unit_name = "not_a_real_unit_of_measure"

  def test_name__is_unique(self,) -> None:
    unit = PackagingUnit(name=self.mocked_unit_name)
    unit.save()

    with pytest.raises(ValidationError) as exc:
      unit2 = PackagingUnit(name=self.mocked_unit_name)
      unit2.save()

    assert str(exc.value) == str(
        {
            '__all__':
                [
                    'Constraint '
                    f'“{CONSTRAINT_NAMES["name"]}” '
                    'is violated.',
                ]
        }
    )

  def test_str__returns_unit_name(self,) -> None:

    unit = PackagingUnit(name=self.mocked_unit_name)

    assert str(unit) == self.mocked_unit_name
