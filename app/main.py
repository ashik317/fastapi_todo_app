from fastapi import FastAPI
from app.routers import todo

app = FastAPI()

app.include_router(todo.router)