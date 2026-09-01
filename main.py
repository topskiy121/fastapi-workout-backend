from contextlib import asynccontextmanager
from database import create_tables
from fastapi import FastAPI, HTTPException, status
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
@app.delete("/workouts/{workout_id}")
async def delete_workout_by_id(workout_id: int):
    deleted_count = await WorkoutRepository.delete_workout_by_id(workout_id)
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="Workout not found")
    return {"status": "deleted"}
@app.get("/workouts/{workout_id}")
async def get_workouts_by_id(workout_id: int):
    workout = await WorkoutRepository.get_workouts_by_id(workout_id)
    if workout is None:
        raise HTTPException(status_code=404, detail="Workout not found")
    return workout
@app.put("/workouts/{workout_id}")
async def update_workout_by_id(workout_id: int, workout: SWorkoutAdd):
    updated_count = await WorkoutRepository.update_workout_by_id(workout_id, workout)
    if updated_count == 0:
        raise HTTPException(status_code=404, detail="Workout not found")
    return{"status": "update"}