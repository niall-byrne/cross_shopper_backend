"""Test the base admin site context processor."""

import pytest
from django.http import HttpRequest
from django.test import override_settings
from utilities.admin.context_processors import base


class TestBaseAdminContextProcessor:

  @pytest.mark.parametrize("environment_name", ('env1', 'env2'))
  def test_vary_environment_name__returns_correct_context(
      self,
      mocked_request: HttpRequest,
      environment_name: str,
  ) -> None:
    with override_settings(ENVIRONMENT=environment_name):
      assert base(mocked_request) == {
          "ENVIRONMENT": environment_name,
      }
