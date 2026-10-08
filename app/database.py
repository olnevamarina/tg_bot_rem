from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

# Database URL: we use SQLite with the aiosqlite async driver
DATABASE_URL = "sqlite+aiosqlite:///./reminders.db"

# Engine: the actual connection pool
engine = create_async_engine(DATABASE_URL, echo=True)  
# (echo=True will print raw SQL queries to your terminal so you can see what happens!)

# Session Factory: creates a fresh session for each operation
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# Dependency: gives a route handler a session, then closes it automatically
async def get_db():
    async with async_session() as session:
        yield session