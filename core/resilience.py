import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from core.config import settings

async def wait_for_db():
    try:
        engine = create_async_engine(settings.DATABASE_URL, connect_args={"prepared_statement_cache_size": 0})
        for i in range(20):
            try:
                async with engine.connect() as conn:
                    await conn.execute(text("SELECT 1"))
                await engine.dispose()
                return True
            except:
                await asyncio.sleep(2)
        await engine.dispose()
    except:
        pass
    return False

async def wait_for_rabbitmq():
    await asyncio.sleep(2)
    return True
