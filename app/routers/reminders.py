from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import Reminder, Template
from app.schemas import ReminderCreate
from app.scheduler import schedule_reminder

router = APIRouter(prefix="/reminders", tags=["Reminders"])

@router.post("", status_code=201)
async def create_reminder(data: ReminderCreate, db: AsyncSession = Depends(get_db)):
    # 1. Resolve text (from template or custom text)
    reminder_text = data.custom_text
    if data.template_id:
        template = await db.get(Template, data.template_id)
        if template:
            reminder_text = template.text
            
    if not reminder_text:
        raise HTTPException(status_code=400, detail="Must provide custom_text or a valid template_id")

    # 2. Save record to DB
    new_reminder = Reminder(
        chat_id=data.chat_id,
        template_id=data.template_id,
        custom_text=data.custom_text,
        reminder_type=data.reminder_type,
        run_at=data.run_at,
        is_active=True
    )
    db.add(new_reminder)
    await db.commit()

    # 3. Schedule the background timer!
    schedule_reminder(
        chat_id=data.chat_id,
        text=reminder_text,
        run_at=data.run_at
    )

    return {"status": "scheduled", "run_at": data.run_at}