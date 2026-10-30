from contextlib import asynccontextmanager
from database import create_tables
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from router import router as workouts_router
import time
from auth_router import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app=FastAPI(lifespan=lifespan)

app.include_router(auth_router)

# Список адресов, которым мы разрешаем делать запросы к API
origins=[
    "http://localhost:3000", # Наш будуший фронтенд (React / Vue)
    "http://127.0.0.1:3000",
    # "*" так можно разрешить вообще всем сайтам (удобно для разработки)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # Разрешеный сайты
    allow_credentials=True, # Разрешаем куки и авторизацию
    allow_methods=["*"], # Разрешаем все HTTP методы get post pu delete...
    allow_headers=["*"], # Разрешаем любые заголовки
)

app.include_router(workouts_router)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time=time.time() # засекаем время на входе 

    response=await call_next(request) # Передаем запрос дальше в роут

    process_time=time.time() - start_time # считаем сколько прошло
    
    client_ip=request.client.host if request.client else "unknown"
    
    print(
        f"[{request.method}] {request.url.path} | "
        f"IP: {client_ip} | "
        f"Status: {response.status_code} | "
        f"Time: {process_time:.4f}s"
    )

    # добавляем время в заголовки ответа
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Как это работает:
# request — пришедший запрос от пользователя (например, GET /workouts).
# call_next(request) — функция, которая отправляет запрос дальше в наш workouts_router и ждёт ответ.
# Всё, что написанo ДО call_next — выполняется до обработки запроса.
# Всё, что написанo ПОСЛЕ call_next — выполняется перед отправкой ответа клиенту.