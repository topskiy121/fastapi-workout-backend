from database import new_session
from models import WorkoutTable
from schemas import SWorkoutAdd
from sqlalchemy import select, delete, update

class WorkoutRepository:
    @classmethod
    async def add_workout(cls, data: SWorkoutAdd,user_id: int) -> int:
        async with new_session() as session:
            workout_dict=data.model_dump()
            workout_dict["user_id"]=user_id
            workout = WorkoutTable(**workout_dict)
            session.add(workout)
            await session.flush()
            await session.commit()
            return workout.id
    @classmethod
    async def get_workouts(cls, user_id: int):
        async with new_session() as session:
            query=select(WorkoutTable).where(WorkoutTable.id == user_id)
            result=await session.execute(query)
            workouts=result.scalars().all()
            return workouts
    @classmethod
    async def delete_workout_by_id(cls, workout_id: int):
        async with new_session() as session:
            query = delete(WorkoutTable).where(WorkoutTable.id == workout_id)
            result = await session.execute(query)
            await session.commit()
            return result.rowcount
    @classmethod
    async def get_workouts_by_id(cls, workout_id: int):
        async with new_session() as session:
            query = select(WorkoutTable).where(WorkoutTable.id == workout_id)
            result = await session.execute(query)
            workout = result.scalar_one_or_none()
            return workout
    @classmethod
    async def update_workout_by_id(cls, workout_id: int, data: SWorkoutAdd):
        async with new_session() as session:
            query = (
                update(WorkoutTable)
                .where(WorkoutTable.id == workout_id)
                .values(**data.model_dump())
                )
            result = await session.execute(query)
            await session.commit()
            return result.rowcount