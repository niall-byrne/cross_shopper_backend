"""Tests for the PassThroughFilter."""

from unittest.mock import Mock

import pytest
from utilities.views.filters.pass_through import PassThroughFilter


class TestPassThroughFilter:
  """Tests for the PassThroughFilter."""

  def test_filter__field_name_provided__request_updated(
      self,
      pass_through_filter: PassThroughFilter,
      request_with_query_params: Mock,
      monkeypatch: "pytest.MonkeyPatch",
  ) -> None:
    monkeypatch.setattr(
        pass_through_filter,
        'get_request',
        Mock(return_value=request_with_query_params),
    )
    qs = Mock()
    result = pass_through_filter.filter(qs, 'test_value')

    assert result == qs
    assert request_with_query_params.GET['test_field'] == 'test_value'
    assert request_with_query_params.GET['existing'] == 'value'

  def test_label__label_provided__correct_label(
      self,
  ) -> None:
    filter_instance = PassThroughFilter(
        field_name='test_field',
        label='Test Label',
    )

    assert filter_instance.label == 'Test Label'

  def test_label__no_label_provided__correct_default_label(
      self,
  ) -> None:
    mock_model = Mock()
    mock_field = Mock()
    mock_field.verbose_name = "Mock model"
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
