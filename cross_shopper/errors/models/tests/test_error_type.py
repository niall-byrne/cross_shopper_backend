"""Test the ErrorType model."""

import pytest
from django.core.exceptions import ValidationError
from errors.models.error_type import CONSTRAINT_NAMES, ErrorType


@pytest.mark.django_db
class TestErrorType:
  mocked_error_type_name = "not_a_real_error"

  def test_name__is_unique(self,) -> None:
    brand = ErrorType(name=self.mocked_error_type_name)
    brand.save()

    with pytest.raises(ValidationError) as exc:
      brand2 = ErrorType(name=self.mocked_error_type_name)
      brand2.save()

    assert str(exc.value) == str(
        {"__all__": [f"Constraint “{CONSTRAINT_NAMES['name']}” is violated.",]}
    )

  def test_str__returns_error_name(self,) -> None:
    error = ErrorType(name=self.mocked_error_type_name)

    assert str(error) == self.mocked_error_type_name
