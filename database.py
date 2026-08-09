import aiosqlite
DB_PATH="workout.db"
async def init_db():
    async with aiosqlite.connect(DB_PATH) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(
                """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL
            );
            """
            )
            await conn.commit()