import asyncio
from database import engine
from sqlalchemy import text

async def drop_alembic_table():
    async with engine.begin() as conn:
        # Принудительно сносим служебную таблицу Alembic
        await conn.execute(text("DROP TABLE IF EXISTS alembic_version CASCADE;"))
    print("Таблица alembic_version успешно удалена!")

asyncio.run(drop_alembic_table())