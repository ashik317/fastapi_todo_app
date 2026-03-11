# Registation and authentication routes for the FastAPI ToDo app
from fastapi import APIRouter, Depends, HTTPException, status, Request, FastAPI
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.main import pwd_context

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("/register", response_class=FastAPI.responses.HTMLResponse)
def register_form(request: Request):
    return FastAPI.responses.HTMLResponse(
        content=FastAPI.templating.Jinja2Templates(directory="app/templates").get_template("register.html").render(),
        status_code=status.HTTP_200_OK
    )

@router.post("/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = pwd_context.hash(user.password)
    new_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user