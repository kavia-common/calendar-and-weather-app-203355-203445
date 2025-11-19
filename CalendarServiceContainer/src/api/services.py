from typing import List
from datetime import datetime, timedelta
from .models import EventModel
from .clients import NotificationClient  # Import directly from clients.py, never via __init__

# PUBLIC_INTERFACE
def expand_event_recurrence(event: EventModel, range_start: datetime, range_end: datetime) -> List[EventModel]:
    """
    Expands a recurring event into a list of event instances within the given date range.
    For BASIC demo: Handles only FREQ=DAILY/WEEKLY and interval; ignores complex rules.
    """
    if not event.recurrence or event.recurrence.get("freq", "NONE") == "NONE":
        # No recurrence, only include if overlaps
        if event.start_time > range_end or event.end_time < range_start:
            return []
        return [event]

    events = []
    freq = event.recurrence.get("freq", "NONE")
    interval = int(event.recurrence.get("interval", 1))
    until = event.recurrence.get("until", None)
    if isinstance(until, str):
        until = datetime.fromisoformat(until)
    first_dt = event.start_time
    i = 0
    current = first_dt
    while True:
        # Only until the range
        if (until and current > until) or current > range_end:
            break
        # Add if instance is in window
        end_instance = current + (event.end_time - event.start_time)
        if end_instance >= range_start and current <= range_end:
            instance_copy = EventModel(**{**event.__dict__, "start_time": current, "end_time": end_instance})
            events.append(instance_copy)
        # Next occurrence
        if freq == "DAILY":
            current += timedelta(days=interval)
        elif freq == "WEEKLY":
            current += timedelta(weeks=interval)
        else:
            break
        i += 1
        if i > 1000:
            break  # failsafe
    return events

# PUBLIC_INTERFACE
def schedule_event_reminders(event: EventModel, notification_client: NotificationClient):
    """
    Emits reminder intents for the given event at the appropriate times before start.
    """
    scheduled_times = []
    for mins in event.reminders:
        reminder_at = event.start_time - timedelta(minutes=mins)
        scheduled_times.append(reminder_at)
    # Emit reminder intents for external notifier (stub for now)
    notification_client.send_reminder_intent(event.id, scheduled_times)
