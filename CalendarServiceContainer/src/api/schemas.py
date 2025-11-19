from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from pydantic import BaseModel, Field, validator

# PUBLIC_INTERFACE
class RecurrenceRule(BaseModel):
    freq: str = Field(..., description="Recurrence frequency (e.g., DAILY, WEEKLY)")
    interval: Optional[int] = Field(1, description="Repeat interval, must be >= 1")
    byweekday: Optional[List[int]] = Field(None, description="List of weekdays [0=Monday, ...] (for WEEKLY)")
    until: Optional[datetime] = Field(None, description="Recurrence ends at this datetime")

    @validator('freq')
    def freq_must_be_known(cls, v):
        allowed = {"DAILY", "WEEKLY", "NONE"}
        if v not in allowed:
            raise ValueError(f"Invalid frequency: {v}")
        return v

    @validator('interval')
    def interval_positive(cls, v):
        if v is not None and v < 1:
            raise ValueError("interval must be >= 1")
        return v


class EventBase(BaseModel):
    title: str = Field(..., description="Title of the event")
    description: Optional[str] = Field(None, description="Description")
    start_time: datetime = Field(..., description="Start datetime")
    end_time: datetime = Field(..., description="End datetime")
    timezone: str = Field(..., description="Timezone, must be a valid tz database name, e.g., 'UTC'")
    location: Optional[str] = Field(None, description="Event location")
    all_day: Optional[bool] = Field(False, description="If the event lasts all day")
    recurrence: Optional[Union[RecurrenceRule, Dict[str, Any], str]] = Field(
        None, description="Recurrence rule, RRULE string, or dict"
    )
    reminders: Optional[List[int]] = Field(default_factory=list, description="List of reminders in minutes before event")


    # Pydantic v2.x pattern: use @model_validator instead of @root_validator
    from pydantic import model_validator

    @model_validator(mode="after")
    def check_times(self):
        start = self.start_time
        end = self.end_time
        tz = self.timezone
        if end is not None and start is not None:
            if end <= start:
                raise ValueError("end_time must be after start_time")
        if tz:
            try:
                import pytz
            except ImportError:
                raise RuntimeError(
                    "pytz is required for timezone validation. Please ensure it is installed."
                )
            try:
                pytz.timezone(tz)
            except Exception:
                raise ValueError(f"{tz} is not a valid timezone string")
        return self

    @validator('reminders', each_item=True)
    def non_negative_reminder(cls, v):
        if v is not None and v < 0:
            raise ValueError("Reminders must be >= 0 (minutes before event)")
        return v

# PUBLIC_INTERFACE
class EventCreate(EventBase):
    user_id: str = Field(..., description="ID of the user creating the event")


# PUBLIC_INTERFACE
class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    timezone: Optional[str] = None
    location: Optional[str] = None
    all_day: Optional[bool] = None
    recurrence: Optional[Union[RecurrenceRule, Dict[str, Any], str]] = None
    reminders: Optional[List[int]] = None
    weather_context: Optional[Dict[str, Any]] = None

# PUBLIC_INTERFACE
class EventRead(EventBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    weather_context: Optional[Dict[str, Any]] = None

    class Config:
        orm_mode = True


class PaginatedEventResponse(BaseModel):
    total: int
    items: List[EventRead]


class EventFilterParams(BaseModel):
    user_id: Optional[str]
    date_from: Optional[datetime]
    date_to: Optional[datetime]
    page: Optional[int] = 1
    page_size: Optional[int] = 20
    include_weather: Optional[bool] = False
