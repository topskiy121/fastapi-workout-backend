from fastapi import APIRouter
from schemas import SUserRegister
from models import UserTable
from auth import get_password_hash
from database import new_session

router=APIRouter(
    prefix="/auth",
    tags=["Авторизация"]
)

@router.post("/register")
async def register_user(user_data: SUserRegister):
    hashed_pwd=get_password_hash(user_data.password)

    new_user=UserTable(
        email=user_data.email,
        hashed_password=hashed_pwd
    )

    async with new_session() as session:
        session.add(new_user)
        await session.commit()

    return{"message": "Пользователь успешно зарегистрирован!"}