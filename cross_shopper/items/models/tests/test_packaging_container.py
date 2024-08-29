"""Test the PackagingContainer model."""

import pytest
from django.core.exceptions import ValidationError
from items.models.packaging_container import (
    CONSTRAINT_NAMES,
    PackagingContainer,
)


@pytest.mark.django_db
class TestPackagingContainer:
  mocked_container_name = "not_a_real_container"

  def test_name__is_unique(self,) -> None:
    container = PackagingContainer(name=self.mocked_container_name)
    container.save()

    with pytest.raises(ValidationError) as exc:
      container2 = PackagingContainer(name=self.mocked_container_name)
      container2.save()

    assert str(exc.value) == str(
        {"__all__": [f"Constraint “{CONSTRAINT_NAMES['name']}” is violated.",]}
    )

  def test_str__returns_container_name(self,) -> None:
    container = PackagingContainer(name=self.mocked_container_name)

    assert str(container) == self.mocked_container_name
