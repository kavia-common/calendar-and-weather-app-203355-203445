from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime

# PUBLIC_INTERFACE
@dataclass
class EventModel:
    """Core event data model for storage and business logic."""
    id: str
    user_id: str
    title: str
    description: Optional[str]
    start_time: datetime
    end_time: datetime
    timezone: str
    location: Optional[str]
    all_day: bool = False
    recurrence: Optional[Dict[str, Any]] = None  # {"freq": "DAILY"/"WEEKLY", "interval": 1, ...}
    reminders: List[int] = field(default_factory=list)  # Minutes before
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    weather_context: Optional[Dict[str, Any]] = None  # Populated optionally

    def __post_init__(self):
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be after start_time")


@dataclass
class RRULE:
    """Simple structure for recurrence, can be enhanced for complex rules."""
    freq: str  # DAILY, WEEKLY, ...
    interval: int = 1
    byweekday: Optional[List[int]] = None  # Monday=0
    until: Optional[datetime] = None
