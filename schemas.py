from pydantic import BaseModel, EmailStr

class SWorkoutAdd(BaseModel):
    title: str
    description: str | None = None

class SWorkout(SWorkoutAdd):
    id: int
    description:str | None = None

class SUserRegister(BaseModel):
    email: EmailStr
    password: str

class SUserAuth(BaseModel):
    email: EmailStr
    password: str