from sqlalchemy.orm import Mapped, mapped_column
from database import Model

class WorkoutTable(Model):
    __tablename__="workouts"

    id: Mapped[int]=mapped_column(primary_key=True)
    title: Mapped[str] 
    description:Mapped[str] = Mapped[str|None]