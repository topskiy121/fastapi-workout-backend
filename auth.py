from pwdlib import PasswordHash

# Инициализируем хэшер паролей с алгоритмом bcrypt
password_hash=PasswordHash.recommended()

def get_password_hash(password: str) -> str:
    # Из сырого пароля в защищенный хэш
    return password_hash.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Проверет совпадает ли введенный пароль с хэшем из базы
    return password_hash.verify(plain_password, hashed_password)