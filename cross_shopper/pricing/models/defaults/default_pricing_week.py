"""Default value for a Price model's week field."""

from datetime import timedelta

from django.utils import timezone
from pricing.constants import DAY_OF_WEEK_FOR_PRICING


def default_pricing_week() -> int:
  """Generate the current isoweek offset by the pricing day."""
  today = timezone.now()
  if today.weekday() >= DAY_OF_WEEK_FOR_PRICING:
    if (today + timedelta(weeks=1)).year > today.year:
      return 1
    else:
      return today.isocalendar().week + 1
  return today.isocalendar().week
