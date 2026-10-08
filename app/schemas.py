from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from app.models import ReminderType

# --- Template Schemas ---

class TemplateCreate(BaseModel):
    text: str = Field(..., max_length=500, example="Remember to drink a glass of water!")

class TemplateResponse(TemplateCreate):
    id: int

    class Config:
        from_attributes = True


# --- Reminder Schemas ---

class ReminderCreate(BaseModel):
    chat_id: int
    template_id: Optional[int] = None
    custom_text: Optional[str] = Field(None, max_length=500)
    
    reminder_type: ReminderType = ReminderType.ONCE
    run_at: datetime  # ISO format string: "2026-09-15T10:00:00"
    
    interval_seconds: Optional[int] = Field(None, ge=10) # Minimum 10 sec interval
    repeat_count: Optional[int] = Field(None, ge=1)      # How many times to repeat