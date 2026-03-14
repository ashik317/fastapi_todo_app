from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserList(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True

class TaskCreate(BaseModel):
    title: str
    description: str = None
    completed: bool = False
    owner_id: int

class TaskResponse(BaseModel):
    title: str
    description: str = None
    completed: bool = False
    owner_id: int

    class Config:
        orm_mode = True
