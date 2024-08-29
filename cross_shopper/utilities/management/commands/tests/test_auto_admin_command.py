"""Test the autoadmin management command."""
import io
from unittest import mock

import pytest
from django.core.management import CommandError, call_command
from utilities.management.commands import autoadmin


class TestAutoAdmin:

  def test_autoadmin__non_existing__shows_success_message(
      self,
      mocked_create_superuser: mock.Mock,
      mocked_stderr: io.StringIO,
      mocked_stdout: io.StringIO,
  ) -> None:
    call_command(
        'autoadmin',
        stdout=mocked_stdout,
        stderr=mocked_stderr,
        no_color=True,
    )

    assert "" == mocked_stderr.getvalue()
    assert autoadmin.SUCCESS_MESSAGE in mocked_stdout.getvalue()

  def test_autoadmin__non_existing__calls_create_superuser(
      self,
      mocked_create_superuser: mock.Mock,
      mocked_stderr: io.StringIO,
      mocked_stdout: io.StringIO,
  ) -> None:
    call_command(
        'autoadmin',
        stdout=mocked_stdout,
        stderr=mocked_stderr,
        no_color=True,
    )

    mocked_create_superuser.assert_called_once_with()

  def test_autoadmin__existing__show_no_content(
      self,
      mocked_create_superuser: mock.Mock,
      mocked_stderr: io.StringIO,
      mocked_stdout: io.StringIO,
  ) -> None:
    mocked_exception = Exception("Error")
    mocked_create_superuser.side_effect = mocked_exception

    with pytest.raises(CommandError):
      call_command(
          'autoadmin',
          stdout=mocked_stdout,
          stderr=mocked_stderr,
          no_color=True
      )

    assert "" == mocked_stderr.getvalue()
    assert "" == mocked_stdout.getvalue()

  def test_autoadmin__existing__raises_exception(
      self,
      mocked_create_superuser: mock.Mock,
      mocked_stderr: io.StringIO,
      mocked_stdout: io.StringIO,
  ) -> None:
    mocked_exception = Exception("Error")
    mocked_create_superuser.side_effect = mocked_exception

    with pytest.raises(CommandError) as exc:
      call_command(
          'autoadmin',
          stdout=mocked_stdout,
          stderr=mocked_stderr,
          no_color=True
      )

    assert str(exc.value) == mocked_exception.args[0]
