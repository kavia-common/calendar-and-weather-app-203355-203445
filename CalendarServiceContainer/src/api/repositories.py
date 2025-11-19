from typing import List, Optional, Dict, Any
from datetime import datetime
from .models import EventModel

# PUBLIC_INTERFACE
class Repository:
    """Repository interface for events."""

    def get(self, event_id: str) -> Optional[EventModel]:
        raise NotImplementedError

    def list(
        self, user_id: Optional[str] = None, date_from: Optional[datetime] = None, date_to: Optional[datetime] = None, skip=0, limit=20
    ) -> List[EventModel]:
        raise NotImplementedError

    def create(self, event: EventModel) -> EventModel:
        raise NotImplementedError

    def update(self, event_id: str, update: Dict[str, Any]) -> Optional[EventModel]:
        raise NotImplementedError

    def delete(self, event_id: str) -> bool:
        raise NotImplementedError


# PUBLIC_INTERFACE
class InMemoryRepository(Repository):
    """Simple in-memory implementation for development/testing."""

    def __init__(self):
        self.events: Dict[str, EventModel] = {}

    def get(self, event_id: str) -> Optional[EventModel]:
        return self.events.get(event_id)

    def list(
        self, user_id: Optional[str] = None, date_from: Optional[datetime] = None, date_to: Optional[datetime] = None, skip=0, limit=20
    ) -> List[EventModel]:
        results = list(self.events.values())
        if user_id:
            results = [e for e in results if e.user_id == user_id]
        if date_from:
            results = [e for e in results if e.start_time >= date_from]
        if date_to:
            results = [e for e in results if e.end_time <= date_to]
        return results[skip : skip + limit]

    def create(self, event: EventModel) -> EventModel:
        self.events[event.id] = event
        return event

    def update(self, event_id: str, update: Dict[str, Any]) -> Optional[EventModel]:
        event = self.events.get(event_id)
        if not event:
            return None
        for k, v in update.items():
            if hasattr(event, k) and v is not None:
                setattr(event, k, v)
        event.updated_at = datetime.utcnow()
        self.events[event_id] = event
        return event

    def delete(self, event_id: str) -> bool:
        if event_id in self.events:
            del self.events[event_id]
            return True
        return False

# PUBLIC_INTERFACE
def get_repository():
    """Returns default repository, update this for DB integration."""
    # Eventually use env/db, for now use in-memory singleton
    if not hasattr(get_repository, "_inst"):
        get_repository._inst = InMemoryRepository()
    return get_repository._inst
