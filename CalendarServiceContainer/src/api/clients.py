from typing import Any, Dict, List
from datetime import datetime

# PUBLIC_INTERFACE
class WeatherClient:
    """Stub for weather integration."""
    def get_forecast_at(self, location: str, dt: datetime) -> Dict[str, Any]:
        """
        Fetches weather for a location at a specific datetime.
        Placeholder: returns dummy weather.
        """
        # TODO: Integrate with real weather service (use Weather Service Container)
        return {
            "location": location,
            "datetime": dt.isoformat(),
            "forecast": "sunny",
            "temperatureC": 22.0
        }

# PUBLIC_INTERFACE
class NotificationClient:
    """Stub for notification integration."""
    def send_reminder_intent(self, event_id: str, schedule_times: List[datetime]):
        """
        Sends a reminder scheduling intent for event.
        Placeholder: no-op, just log. Eventually call Notification Service.
        """
        # TODO: Integrate with Notification Service Container
        # For demo, just print (could log)
        print(f"[NotificationClient] Would send reminders for event {event_id} at {schedule_times}")
