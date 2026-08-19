from contextlib import asynccontextmanager
from database import create_tables
from fastapi import FastAPI
from schemas import SWorkoutAdd
from repository import WorkoutRepository

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield

app=FastAPI(lifespan=lifespan)

@app.post("/workouts")
async def add_workout(workout: SWorkoutAdd):
    workout_id = await WorkoutRepository.add_workout(workout)
    return {"ok": True, "workout_id": workout_id}
@app.get("/workouts")
async def get_workouts():
    workouts=await WorkoutRepository.get_workouts()
    return workouts