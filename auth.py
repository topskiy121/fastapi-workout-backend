from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
import jwt 
# Инициализируем хэшер паролей с алгоритмом bcrypt
password_hash=PasswordHash.recommended()

SECRET_KEY="my_super_secret_key123" # Ключ известный только серверу
ALGORITHM="HS256"


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