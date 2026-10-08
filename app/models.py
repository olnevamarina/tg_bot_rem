from enum import Enum as PyEnum
from datetime import datetime
from typing import Optional
from sqlalchemy import String, BigInteger, DateTime, Enum, Integer, Boolean, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass
# 1. Define reminder types
class ReminderType(str, PyEnum):
    ONCE = "once"              # Fires once at a specific date/time
    INTERVAL = "interval"      # Fires every N minutes/hours for X count
    UNTIL_STOP = "until_stop"  # Fires endlessly until is_active becomes False

class Template(Base):
    __tablename__ = "templates"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(String(500), nullable=False)

class Reminder(Base):
    __tablename__ = "reminders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    
    # Optional link to a pre-saved template
    template_id: Mapped[Optional[int]] = mapped_column(ForeignKey("templates.id"), nullable=True)
    custom_text: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Core Scheduling Fields
    reminder_type: Mapped[ReminderType] = mapped_column(Enum(ReminderType), default=ReminderType.ONCE)
    run_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)  # First/next execution time
    
    # Repeating Logic
    interval_seconds: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # E.g., 3600 for every hour
    repeat_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)      # E.g., 3 times total (None = infinite)
    times_fired: Mapped[int] = mapped_column(Integer, default=0)

    # Active State ("until I say stop")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)