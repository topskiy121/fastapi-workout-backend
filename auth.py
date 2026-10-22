from sqlalchemy import select
from models import UserTable
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
import jwt
# Инициализируем хэшер паролей с алгоритмом bcrypt
password_hash=PasswordHash.recommended()

SECRET_KEY="my_super_secret_key123" # Ключ известный только серверу
ALGORITHM="HS256"

OAuth2_PasswordBearer_schema=OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_password_hash(password: str) -> str:
    # Из сырого пароля в защищенный хэш
    return password_hash.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Проверет совпадает ли введенный пароль с хэшем из базы
    return password_hash.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode=data.copy() # Копируем переданный словарь

    expire=datetime.now(timezone.utc)+timedelta(minutes=30) # Вычисляем время тушения токена (текущее время UTC + 30 минут)
    to_encode.update({"exp": expire}) # Добавляем системное поле "exp" (expiration — срок годности)

    # Кодируем в JWT с помощью секретного ключа
    encoded_jwt=jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(
    token:str=Depends(OAuth2_PasswordBearer_schema),
    session: AsyncSession=Depends(get_db)
):  

    try:
        decoded_jwt=jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id=decoded_jwt.get("sub")
        
        user_id=int(user_id)
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
            )
    result=await session.execute(
        select(UserTable)
        .where(UserTable.id==user_id))
    user=result.scalar_one_or_none()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
                    )
    user_id=int(user_id)
    return user
