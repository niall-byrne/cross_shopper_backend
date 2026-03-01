"""Tests for the PassThroughFilter."""

from unittest.mock import Mock

from django.http import QueryDict
from ..pass_through import PassThroughFilter


class TestPassThroughFilter:
  """Tests for the PassThroughFilter."""

  def test_filter__updates_request_get(self) -> None:
    """Test that the filter correctly updates the request's GET parameters."""
    request = Mock()
    request.GET = QueryDict('', mutable=True)
    request.GET.update({'existing': 'value'})

    # Mock get_request to return our mock request
    filter_instance = PassThroughFilter(field_name='test_field')
    filter_instance.get_request = Mock(return_value=request)

    # Calling filter should update request.GET
    qs = Mock()
    result = filter_instance.filter(qs, 'test_value')

    assert result == qs
    assert request.GET['test_field'] == 'test_value'
    assert request.GET['existing'] == 'value'

  def test_label(self) -> None:
    """Test the label method of PassThroughFilter."""
    filter_instance = PassThroughFilter(
        field_name='test_field', label='Test Label'
    )
    # label is a property on the filter, but PassThroughFilter doesn't override it in a way
    # that makes it a method. CharFilter.label is a property.
    assert filter_instance.label == 'Test Label'

  def test_init__sets_model(self) -> None:
    """Test that the model is correctly set in __init__."""
    mock_model = Mock()
    filter_instance = PassThroughFilter(for_model=mock_model)
    assert filter_instance.model == mock_model
