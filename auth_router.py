from sqlalchemy import select
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, HTTPException, status, Depends
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
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    async with new_session() as session:
        query=(
            select(UserTable)
            # OAuth2 форма всегда передает логин в поле username, даже если мы вводим туда email
            .where(UserTable.email == form_data.username) 
        )
        result=await session.execute(query)
        user=result.scalar_one_or_none()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Неверный email или пароль"
                )
    access_token=create_access_token(data={"sub": str(user.id)})
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }