from contextlib import asynccontextmanager
from fastapi import FastAPI
import aiosqlite

from database import DB_PATH, init_db
from schemas import UserCreate, UserResponse

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app= FastAPI(lifespan=lifespan)

@app.post("/user/", response_model=UserResponse)
async def create_user(user: UserCreate):
    async with aiosqlite.connect(DB_PATH) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(
                "INSERT INTO users (name, age) VALUES (?, ?);",
                (user.name, user.age),
            )
            await conn.commit()
            user_id=cursor.lastrowid
    return {"id": user_id, "name": user.name, "age": user.age}
@app.get("/users/", response_model=list[UserResponse])
async def read_user():
    async with aiosqlite.connect(DB_PATH) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(
                "SELECT * FROM users"
            )
            result= await cursor.fetchall()
        history=[{"id": row[0], "name": row [1], "age": row [2]} for row in result]
        return history
@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    async with aiosqlite.connect(DB_PATH) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(
                "DELETE FROM users WHERE id=?", (id,)
            )
            await conn.commit()
    return {"status": "success", "id": id}