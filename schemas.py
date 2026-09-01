from pydantic import BaseModel

class SWorkoutAdd(BaseModel):
    title: str
    description: str | None = None

class SWorkout(SWorkoutAdd):
    id: int