from auth import get_current_user
from models import UserTable
from fastapi import APIRouter, HTTPException, status, Depends
from schemas import SWorkoutAdd
from repository import WorkoutRepository

router = APIRouter(
    prefix="/workouts",
    tags=["Workouts"]
)

@router.post("", status_code=status.HTTP_201_CREATED)
async def add_workout(workout: SWorkoutAdd, current_user: UserTable=Depends(get_current_user)):
    workout_id = await WorkoutRepository.add_workout(workout, current_user.id)
    return {"ok": True, "workout_id": workout_id}

@router.get("")
async def get_workouts():
    workouts = await WorkoutRepository.get_workouts()
    return workouts

@router.get("/{workout_id}")
async def get_workouts_by_id(workout_id: int):
    workout = await WorkoutRepository.get_workouts_by_id(workout_id)
    if workout is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Workout not found"
        )
    return workout

@router.put("/{workout_id}")
async def update_workout_by_id(workout_id: int, workout: SWorkoutAdd):
    updated_count = await WorkoutRepository.update_workout_by_id(workout_id, workout)
    if updated_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Workout not found"
        )
    return {"status": "update"}

@router.delete("/{workout_id}")
async def delete_workout_by_id(workout_id: int):
    deleted_count = await WorkoutRepository.delete_workout_by_id(workout_id)
    if deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Workout not found"
        )
    return {"status": "deleted"}