from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List, Optional
from uuid import uuid4
from datetime import datetime
from ..schemas import (
    EventCreate,
    EventRead,
    EventUpdate,
    PaginatedEventResponse,
)
from ..models import EventModel
from ..repositories import get_repository, Repository
from ..clients import WeatherClient, NotificationClient
from ..services import expand_event_recurrence, schedule_event_reminders

router = APIRouter(prefix="/events", tags=["Events"])

def get_weather_client():
    return WeatherClient()

def get_notification_client():
    return NotificationClient()

# PUBLIC_INTERFACE
@router.post(
    "", response_model=EventRead, status_code=status.HTTP_201_CREATED, summary="Create an event"
)
def create_event(
    event: EventCreate,
    repo: Repository = Depends(get_repository),
    notification_client: NotificationClient = Depends(get_notification_client),
):
    """
    Create a new calendar event. Triggers reminder scheduling on creation.
    """
    event_id = str(uuid4())
    now = datetime.utcnow()
    model = EventModel(
        id=event_id,
        user_id=event.user_id,
        title=event.title,
        description=event.description,
        start_time=event.start_time,
        end_time=event.end_time,
        timezone=event.timezone,
        location=event.location,
        all_day=event.all_day or False,
        recurrence=event.recurrence.dict() if hasattr(event.recurrence, "dict") else event.recurrence,
        reminders=event.reminders or [],
        created_at=now,
        updated_at=now,
        weather_context=None,
    )
    saved = repo.create(model)
    schedule_event_reminders(saved, notification_client)
    return EventRead(**saved.__dict__)

# PUBLIC_INTERFACE
@router.get(
    "/{event_id}", response_model=EventRead, summary="Get event by ID"
)
def get_event(
    event_id: str,
    repo: Repository = Depends(get_repository),
    include_weather: bool = Query(False, description="If true, include weather context"),
    weather_client: WeatherClient = Depends(get_weather_client)
):
    """
    Retrieve an event by its ID, optionally enriched with weather information.
    """
    event = repo.get(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if include_weather and event.location:
        event.weather_context = weather_client.get_forecast_at(event.location, event.start_time)
    return EventRead(**event.__dict__)

# PUBLIC_INTERFACE
@router.get(
    "",
    response_model=PaginatedEventResponse,
    summary="List events with filters",
)
def list_events(
    user_id: Optional[str] = Query(None),
    date_from: Optional[datetime] = Query(None),
    date_to: Optional[datetime] = Query(None),
    page: int = Query(1, gt=0),
    page_size: int = Query(20, ge=1, le=100),
    include_weather: bool = Query(False, description="If true, include weather context"),
    repo: Repository = Depends(get_repository),
    weather_client: WeatherClient = Depends(get_weather_client)
):
    """
    List events, optionally filtered by user and date range, paginated. Recurring events are expanded appropriately.
    """
    skip = (page - 1) * page_size
    base_events = repo.list(user_id=user_id, date_from=date_from, date_to=date_to)
    events: List[EventModel] = []
    for event in base_events:
        expanded = expand_event_recurrence(event, date_from or datetime.min, date_to or datetime.max)
        events.extend(expanded)
    # Pagination after expansion
    total = len(events)
    paged = events[skip : skip + page_size]
    # Weather context
    items = []
    for event in paged:
        if include_weather and event.location:
            event.weather_context = weather_client.get_forecast_at(event.location, event.start_time)
        items.append(EventRead(**event.__dict__))
    return PaginatedEventResponse(total=total, items=items)

# PUBLIC_INTERFACE
@router.patch(
    "/{event_id}", response_model=EventRead, summary="Update event"
)
def update_event(
    event_id: str,
    patch: EventUpdate,
    repo: Repository = Depends(get_repository),
    notification_client: NotificationClient = Depends(get_notification_client),
):
    """
    Update mutable fields of an event.
    """
    update_data = patch.dict(exclude_unset=True)
    updated = repo.update(event_id, update_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Event not found")
    schedule_event_reminders(updated, notification_client)
    return EventRead(**updated.__dict__)

# PUBLIC_INTERFACE
@router.delete(
    "/{event_id}", status_code=204, summary="Delete event"
)
def delete_event(
    event_id: str,
    repo: Repository = Depends(get_repository),
):
    """
    Delete an event by its ID.
    """
    if repo.delete(event_id):
        return
    raise HTTPException(status_code=404, detail="Event not found")
