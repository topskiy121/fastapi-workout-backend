from pydantic import BaseModel
class SWorkoutAdd(BaseModel):
    title:str
    description:str | None = None
class SWorkout(BaseModel):
    id:int
    name:str
    age:int