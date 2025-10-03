"""Type hints for django-constance."""


class _ConfigStub:

  def __getattribute__(self, name: str) -> str:
    ...


config = _ConfigStub()
