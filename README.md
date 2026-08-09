# FastAPI Async CRUD API

Асинхронное REST API приложение на FastAPI с использованием SQLite (`aiosqlite`) и Pydantic для валидации данных.

## Стек технологий
* **Python 3.11+**
* **FastAPI** — веб-фреймворк
* **aiosqlite** — асинхронная работа с базой данных SQLite
* **Pydantic** — валидация данных и схемы
* **Uvicorn** — ASGI-сервер

## Структура проекта
* `main.py` — маршруты (endpoints) и точка входа FastAPI
* `schemas.py` — Pydantic-схемы для запросов и ответов
* `database.py` — подключение к БД и инициализация таблиц

## Как запустить локально
1. Клонировать репозиторий:
   ```bash
   git clone [https://github.com/topskiy121/fastapi-crud-backend.git](https://github.com/topskiy121/fastapi-crud-backend.git)