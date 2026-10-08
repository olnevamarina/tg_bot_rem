import re
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Reminder, ReminderType
from app.scheduler import schedule_reminder
from app.services import send_telegram_message

router = APIRouter(prefix="/webhook", tags=["Webhook"])

@router.post("")
async def telegram_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    """Handles incoming updates from Telegram."""
    data = await request.json()
    
    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        user_text = data["message"]["text"].strip()
        
        # 1. Handle /start command
        if user_text == "/start":
            welcome_text = (
                "👋 Hello! I am your Reminder Bot.\n\n"
                "You can schedule reminders directly using:\n"
                "• `/remind Water plants in 10 minutes`\n"
                "• `/remind Call Mom in 1 hour`"
            )
            await send_telegram_message(chat_id=chat_id, text=welcome_text)
            return {"status": "ok"}

        # 2. Handle /remind command
        if user_text.startswith("/remind"):
            prompt = user_text.replace("/remind", "", 1).strip()
            
            if not prompt:
                await send_telegram_message(
                    chat_id=chat_id, 
                    text="❌ Please specify a message! Example: `/remind Drink water in 5 minutes`"
                )
                return {"status": "ok"}

            # Parse "in X minutes" or "in X hours"
            delay_minutes = 1  # Default fallback
            clean_text = prompt

            match = re.search(r"in\s+(\d+)\s*(minute|min|hour|hr)s?", prompt, re.IGNORECASE)
            if match:
                amount = int(match.group(1))
                unit = match.group(2).lower()
                
                if unit in ["hour", "hr"]:
                    delay_minutes = amount * 60
                else:
                    delay_minutes = amount
                
                clean_text = prompt[:match.start()].strip()

            if not clean_text:
                clean_text = prompt

            run_at = datetime.now(timezone.utc) + timedelta(minutes=delay_minutes)

            # Save reminder to DB
            new_reminder = Reminder(
                chat_id=chat_id,
                custom_text=clean_text,
                reminder_type=ReminderType.ONCE,
                run_at=run_at,
                is_active=True
            )
            db.add(new_reminder)
            await db.commit()

            # Schedule background task in APScheduler
            schedule_reminder(chat_id=chat_id, text=clean_text, run_at=run_at)

            # Reply with confirmation
            confirm_msg = f"⏰ Reminder set for '{clean_text}' in {delay_minutes} minute(s)!"
            await send_telegram_message(chat_id=chat_id, text=confirm_msg)

    return {"status": "ok"}