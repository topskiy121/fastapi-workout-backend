## Полезные шпаргалки по командам:
- Запуск сервера: `uvicorn main:app --reload`
- Генерация миграции Alembic: `python -m alembic revision --autogenerate -m "commit message"`
- Применение миграции: `python -m alembic upgrade head`