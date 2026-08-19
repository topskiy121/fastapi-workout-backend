from database import new_session
from models import WorkoutTable
from schemas import SWorkoutAdd
from sqlalchemy import select

class WorkoutRepository:
    @classmethod
    async def add_workout(cls, data: SWorkoutAdd) -> int:
        async with new_session() as session:
            workout_dict=data.model_dump()
            workout = WorkoutTable(**workout_dict)
            session.add(workout)
            await session.flush()
            await session.commit()
            return workout.id
    @classmethod
    async def get_workouts(cls):
        async with new_session() as session:
            query=select(WorkoutTable)
            result=await session.execute(query)
            workouts=result.scalars().all()
            return workouts