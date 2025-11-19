"""
PUBLIC_INTERFACE

src/api/main.py -- FastAPI application bootstrap, OpenAPI docs configuration, and router mounting.

This is the primary FastAPI entrypoint:
    - Exposes OpenAPI docs at http://localhost:3001/docs when run via uvicorn or CalendarServiceContainer/main.py
    - Includes core events router and configures demo/test seed data on startup.

Key behaviors:
    * FastAPI instance is assigned to 'app'
    * CORS middleware enables development/test accessibility
    * Routers and health endpoints are registered for complete self-docs

Uvicorn launch command (from container root):
    uvicorn src.api.main:app --host 0.0.0.0 --port 3001 --reload

See README.md for details.
"""
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
# PUBLIC_INTERFACE
app = FastAPI(
    title="CalendarServiceContainer API",
    description="Backend service for calendar, events, recurrence, and reminders with weather and notification integration points.",
    version="0.1.0",
    openapi_tags=openapi_tags
)

# Allow all origins for development and testing; update before production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# PUBLIC_INTERFACE
@app.get("/health", tags=["Health"])
def health_check():
    """Health endpoint to verify service availability."""
    return {"message": "Healthy"}

# Attach event routers for full event/recurrence functionality
app.include_router(events.router)


# Optionally seed repository with sample events if empty (on startup)
@app.on_event("startup")
def seed_events():
    """
    Optionally seeds the event repository with a demo event on startup 
    if no events have yet been created in the current process lifetime.
    """
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
