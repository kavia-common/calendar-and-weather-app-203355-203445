from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import events
from .repositories import get_repository
from datetime import datetime, timedelta
from uuid import uuid4

openapi_tags = [
    {
        "name": "Events",
        "description": "Operations related to calendar events, including CRUD, recurrence, and reminders.",
    }
]
app = FastAPI(
    title="CalendarServiceContainer API",
    description="Backend service for calendar, events, recurrence, and reminders with weather and notification integration points.",
    version="0.1.0",
    openapi_tags=openapi_tags
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For local dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health endpoint (OpenAPI doc root "/" collides with existing, so use "/health")
@app.get("/health", tags=["Health"])
def health_check():
    """Health endpoint to verify service availability."""
    return {"message": "Healthy"}

# Attach event routers.
app.include_router(events.router)


# Optionally seed repository with sample events if empty (on startup)
@app.on_event("startup")
def seed_events():
    repo = get_repository()
    if len(repo.list()) == 0:
        now = datetime.utcnow()
        sample_event = {
            "id": str(uuid4()),
            "user_id": "demo-user",
            "title": "Welcome Event",
            "description": "First launch demo event",
            "start_time": now + timedelta(days=1),
            "end_time": now + timedelta(days=1, hours=1),
            "timezone": "UTC",
            "location": "Online",
            "all_day": False,
            "recurrence": {"freq": "NONE"},
            "reminders": [30],
            "created_at": now,
            "updated_at": now,
            "weather_context": None,
        }
        from .models import EventModel
        repo.create(EventModel(**sample_event))
