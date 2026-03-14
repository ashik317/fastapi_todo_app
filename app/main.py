from fastapi import FastAPI
from app.database import Base, engine

from app.routers import home, task, user

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(home.router)
app.include_router(task.router)
app.include_router(user.router)