from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.services import send_telegram_message

# Global scheduler instance
scheduler = AsyncIOScheduler()

async def execute_reminder_job(chat_id: int, text: str):
    """Callback function executed by APScheduler at the defined time."""
    print(f"⏰ Triggering scheduled reminder for chat {chat_id}...")
    await send_telegram_message(chat_id=chat_id, text=text)

def schedule_reminder(chat_id: int, text: str, run_at: datetime):
    """Schedules a job to run at a specific date and time."""
    scheduler.add_job(
        execute_reminder_job,
        trigger="date",
        run_date=run_at,
        args=[chat_id, text]
    )