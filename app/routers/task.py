from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app import models

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/add")
def add_task(
    request: Request,
    title: str = Form(...),
    description: str = Form(None),
    db: Session = Depends(get_db)
):

    user_id = request.cookies.get("user_id")

    task = models.Todo(
        title=title,
        description=description,
        owner_id=int(user_id)
    )

    db.add(task)
    db.commit()

    return RedirectResponse("/home/", status_code=303)


@router.post("/{task_id}/delete")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):

    task = db.query(models.Todo).filter(models.Todo.id == task_id).first()

    if task:
        db.delete(task)
        db.commit()

    return RedirectResponse("/home/", status_code=303)