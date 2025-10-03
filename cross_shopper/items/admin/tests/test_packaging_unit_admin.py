"""Test the admin for the PackagingUnit model."""

from unittest import mock

from items.admin.packaging_unit import PackagingUnitAdmin


class TestIPackagingUnit:
  """Test the PackagingUnit class."""

  def test_get_ordering__returns_correct_field_order(
      self,
      packaging_unit_admin: PackagingUnitAdmin,
      mocked_request: mock.Mock,
  ) -> None:
    field_order = packaging_unit_admin.get_ordering(mocked_request)

    assert field_order == ('name',)
