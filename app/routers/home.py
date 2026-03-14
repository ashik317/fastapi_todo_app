from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app import models

router = APIRouter(
    prefix="/home",
    tags=["home"]
)

templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    user_id = request.cookies.get("user_id")
    user = None
    tasks = []

    if user_id:
        user = db.query(models.User).filter(models.User.id == int(user_id)).first()
        if user:
            tasks = db.query(models.Todo).filter(models.Todo.owner_id == user.id).all()

    return templates.TemplateResponse(
        "home.html",
        {"request": request, "user": user, "tasks": tasks}
    )