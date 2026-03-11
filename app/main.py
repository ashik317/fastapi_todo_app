from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from app.routers import todo
from fastapi_todo_app.app.database import Base
from .database import engine
from passlib.context import CryptContext

Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app.include_router(todo.router)