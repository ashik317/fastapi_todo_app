# Registation and authentication routes for the FastAPI ToDo app
from fastapi import APIRouter, Depends, HTTPException, status, Request, FastAPI
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.main import pwd_context

router = APIRouter(
    prefix="/users",
    tags=["users"]
)
templates = Jinja2Templates(directory="templates")

@router.get("/register", response_class=FastAPI.responses.HTMLResponse)
def register_form(request: Request):
        return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(
    request: Request,
    username: str = FastAPI.Form(...),
    password: str = FastAPI.Form(...),
    db: Session = Depends(get_db)
):
    if db.query(models.User).filter(models.User.username == username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    
    hashed_password = pwd_context.hash(password)
    new_user = models.User(username=username, password=hashed_password)
    db.add(new_user)
    db.commit()
    return RedirectResponse(url="/users/login", status_code=status.HTTP_303_SEE_OTHER)