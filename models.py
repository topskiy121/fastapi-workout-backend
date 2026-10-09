from sqlalchemy.orm import Mapped, mapped_column
from database import Model

class WorkoutTable(Model):
    __tablename__="workouts"

    id: Mapped[int]=mapped_column(primary_key=True)
    title: Mapped[str] 
    description: Mapped[str | None] = mapped_column(default=None)

class UserTable(Model):
    __tablename__="users"

    id: Mapped[int]=mapped_column(primary_key=True)
    email: Mapped[str]=mapped_column(unique=True, index=True) #unique=True гарантирует что в базе не может быть больше двух пользователей с одинаковым email
    hashed_password: Mapped[str]                              #index=True делает поиск по email молниеносным (индекс БД)