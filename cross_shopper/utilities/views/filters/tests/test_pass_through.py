"""Tests for the PassThroughFilter."""

from unittest.mock import Mock

from django.http import QueryDict
from ..pass_through import PassThroughFilter


class TestPassThroughFilter:
  """Tests for the PassThroughFilter."""

  def test_filter__field_name__request_updated(
      self,
  ) -> None:
    request = Mock()
    request.GET = QueryDict('', mutable=True)
    request.GET.update({'existing': 'value'})
    filter_instance = PassThroughFilter(field_name='test_field')
    filter_instance.get_request = Mock(return_value=request)
    qs = Mock()
    result = filter_instance.filter(qs, 'test_value')

    assert result == qs
    assert request.GET['test_field'] == 'test_value'
    assert request.GET['existing'] == 'value'

  def test_label__label_provided__correct_label(
      self,
  ) -> None:
    filter_instance = PassThroughFilter(
        field_name='test_field',
        label='Test Label',
    )

    assert filter_instance.label == 'Test Label'

  def test_label__no_label_provided__correct_default(
      self,
  ) -> None:
    mock_model = Mock()
    # Mocking the way django-filters extracts the verbose name
    mock_field = Mock()
    mock_field.verbose_name = "mock model"
    mock_model._meta.get_field.return_value = mock_field

    filter_instance = PassThroughFilter(
        field_name='test_field',
        for_model=mock_model,
    )

    assert filter_instance.label == "Mock model"

  def test_init__for_model_provided__sets_model(
      self,
  ) -> None:
    mock_model = Mock()
    filter_instance = PassThroughFilter(for_model=mock_model)

    assert filter_instance.model == mock_model
