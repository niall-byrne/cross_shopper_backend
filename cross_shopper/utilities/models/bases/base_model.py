"""Base Database Model for Cross Shopper."""

from typing import Any

from django.db import models


class BaseModel(models.Model):
  """Inherit from me."""

  class Meta:
    abstract = True

  def save(self, *args: Any, **kwargs: Any) -> None:
    """Clean and save model."""
    self.full_clean()
    super().save(*args, **kwargs)
