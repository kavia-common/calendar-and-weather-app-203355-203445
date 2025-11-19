import pytz
from datetime import datetime

# PUBLIC_INTERFACE
def normalize_dt(dt: datetime, tz_name: str) -> datetime:
    """Ensure a datetime is timezone-aware and in the specified timezone."""
    tz = pytz.timezone(tz_name)
    if dt.tzinfo is None:
        return tz.localize(dt)
    else:
        return dt.astimezone(tz)
