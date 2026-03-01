"""Tests for the PassThroughFilter."""

from unittest.mock import Mock

import pytest
from utilities.views.filters.pass_through import PassThroughFilter


class TestPassThroughFilter:
  """Tests for the PassThroughFilter."""

  def test_filter__field_name_provided__returns_queryset_and_updates_request(
      self,
      pass_through_filter: PassThroughFilter,
      request_with_query_params: Mock,
      monkeypatch: "pytest.MonkeyPatch",
      mock_queryset: Mock,
  ) -> None:
    monkeypatch.setattr(
        pass_through_filter,
        'get_request',
        Mock(return_value=request_with_query_params),
    )
    result = pass_through_filter.filter(mock_queryset, 'test_value')

    assert result == mock_queryset
    assert request_with_query_params.GET['test_field'] == 'test_value'
    assert request_with_query_params.GET['existing'] == 'value'

  def test_label__label_provided__returns_label(
      self,
  ) -> None:
    filter_instance = PassThroughFilter(
        field_name='test_field',
        label='Test Label',
    )

    assert filter_instance.label == 'Test Label'

  def test_label__no_label_provided__returns_model_field_verbose_name(
      self,
      mock_model: Mock,
  ) -> None:
    filter_instance = PassThroughFilter(
        field_name='test_field',
        for_model=mock_model,
    )

    assert filter_instance.label == "Mock model"

  def test_instantiate__for_model_provided__sets_model_attribute(
      self,
      mock_model: Mock,
  ) -> None:
    filter_instance = PassThroughFilter(for_model=mock_model)

    assert filter_instance.model == mock_model
