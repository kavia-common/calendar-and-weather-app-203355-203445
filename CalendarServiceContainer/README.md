# CalendarServiceContainer

This is the backend FastAPI service for managing calendar events, recurrence rules, and reminders. It exposes a REST API to create, update, view, and delete calendar events with support for simple recurring events and event notifications/reminders, as well as placeholder weather context integration.

## Usage

- The service runs on port **3001**.
- Visit [http://localhost:3001/docs](http://localhost:3001/docs) for the OpenAPI auto-generated API docs and test UI.

### Key Endpoints

- `GET /health` — Health check.
- `POST /events` — Create an event.
- `GET /events/{event_id}` — Get an event, optionally with weather info.
- `GET /events` — List events (with date range, user filter, recurrence expansion, pagination, and optional weather).
- `PATCH /events/{event_id}` — Update event.
- `DELETE /events/{event_id}` — Delete event.

### Advanced Features

- **Recurrence:** Use `recurrence` field on event payload with simple FREQ/INTERVAL, e.g. `{"freq": "DAILY", "interval": 1}`.
- **Reminders:** Send minutes-before values in the `reminders` array; see API docs.
- **Weather:** GET endpoints support `include_weather=true` to enrich with dummy weather (stub, to be replaced).
- **Notifications:** When creating/updating events/reminders, notification intent is logged (stub).

### Development

- Default storage is in-memory only (no persistence). See `repositories.py` for adapter point to DB.
- No external API keys required for demo; integrations are stubbed.
- To run:
    ```
    uvicorn src.api.main:app --host 0.0.0.0 --port 3001 --reload
    ```
- On first run, a sample event is seeded for demonstration.

---

## Folder Structure

- `src/api/models.py` — Data models
- `src/api/schemas.py` — Pydantic API schemas
- `src/api/repositories.py` — Repository layer
- `src/api/services.py` — Recurrence/reminder logic
- `src/api/clients.py` — Weather/notification stubs
- `src/api/utils/timezone.py` — Timezone helpers
- `src/api/routers/events.py` — Event API routes
- `src/api/main.py` — App bootstrap (CORS, OpenAPI, routers)

## Environment

- If no `.env` is present, default settings are used.

## Extensibility

- For production, implement DB-backed repository and real notification and weather clients by editing the respective files.
