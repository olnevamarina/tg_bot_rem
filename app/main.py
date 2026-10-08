from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import engine
from app.models import Base
from app.scheduler import scheduler
from app.routers import templates, reminders , webhook

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    scheduler.start()
    print("⏰ APScheduler started!")
    
    yield
    
    # Shutdown
    scheduler.shutdown()
    print("⏰ APScheduler shut down.")

app = FastAPI(title="Reminder Bot", lifespan=lifespan)
app.include_router(templates.router)
app.include_router(reminders.router)
app.include_router(webhook.router)