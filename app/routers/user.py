from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates

from app.database import get_db
from app import models
from app.core.security import hash_password, verify_password

templates = Jinja2Templates(directory="app/templates")

router = APIRouter(prefix="/users", tags=["users"])

# --------------------------
# GET: Show Register Form
# --------------------------
@router.get("/register")
@router.get("/register/")
def register_get(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

# --------------------------
# POST: Handle Register Form
# --------------------------
@router.post("/register")
@router.post("/register/")
def register_post(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    # Check if user exists
    if db.query(models.User).filter(models.User.username == username).first():
        raise HTTPException(status_code=400, detail="Username already exists")

    # Hash password
    hashed_password = hash_password(password)

    # Create new user
    new_user = models.User(
        username=username,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()

    return RedirectResponse("/users/login", status_code=303)


# --------------------------
# GET: Show Login Form
# --------------------------
@router.get("/login")
@router.get("/login/")
def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


# --------------------------
# POST: Handle Login Form
# --------------------------
@router.post("/login")
@router.post("/login/")
def login_post(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.username == username).first()

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    response = RedirectResponse("/home/", status_code=303)
    response.set_cookie(key="user_id", value=str(user.id), httponly=True)

    return response


# --------------------------
# GET: Logout
# --------------------------
@router.get("/logout")
@router.get("/logout/")
def logout():
    response = RedirectResponse("/users/login", status_code=303)
    response.delete_cookie("user_id")
    return response