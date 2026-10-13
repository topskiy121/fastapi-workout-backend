from sqlalchemy import select
from fastapi import APIRouter, HTTPException, status
from schemas import SUserRegister, SUserAuth
from models import UserTable
from auth import get_password_hash, create_access_token, verify_password
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

@router.post("/login")
async def login_user(user_data: SUserAuth):
    async with new_session() as session:
        query=(
            select(UserTable)
            .where(UserTable.email==user_data.email)
        )
        result=await session.execute(query)
        user=result.scalar_one_or_none()



    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Неверный email или пароль"
                )
    access_token=create_access_token(data={"sub": str(user.id)})
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }