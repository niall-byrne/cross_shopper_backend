"""Tests for the PassThroughFilter."""

from typing import TYPE_CHECKING
from unittest import mock
from unittest.mock import Mock

import pytest
from utilities.views.filters.passthrough import PassThroughFilter

if TYPE_CHECKING:  # no cover
  from typing import Any, Dict, Optional


class TestPassThroughFilter:
  """Tests for the PassThroughFilter."""

  @pytest.mark.parametrize('input_value', ('value1', 'value2'))
  def test_filter__field_name_provided__passes_through_queryset(
      self,
      passthrough_filter: "PassThroughFilter",
      mocked_queryset: "Mock",
      input_value: "str",
  ) -> None:
    result = passthrough_filter.filter(mocked_queryset, input_value)

    assert result == mocked_queryset

  @pytest.mark.parametrize('input_value', ('value1', 'value2'))
  def test_filter__field_name_provided__updates_query_params(
      self,
      passthrough_filter: "PassThroughFilter",
      mocked_request_with_query_params: "Mock",
      mocked_queryset: "Mock",
      input_value: "str",
  ) -> None:
    passthrough_filter.filter(mocked_queryset, input_value)

    assert mocked_request_with_query_params.GET['test_field'] == input_value
    assert mocked_request_with_query_params.GET['param'] == 'value'

  @pytest.mark.parametrize(
      'label,model,expected_label',
      (
          ('Test Label', False, 'Test Label'),
          ('Test Label', True, 'Test Label'),
          (None, True, 'Mock model'),
          (None, False, None),
      ),
  )
  def test_label__vary_kwargs__returns_label(
      self,
      mocked_model: "mock.Mock",
      label: "Optional[str]",
      model: "bool",
      expected_label: "Optional[str]",
  ) -> None:
    kwargs: "Dict[str, Any]" = {'field_name': 'test_field'}
    if label:
      kwargs.update({'label': label})
    if model:
      kwargs.update({'for_model': mocked_model})

    filter_instance = PassThroughFilter(**kwargs)

    assert filter_instance.label == expected_label
