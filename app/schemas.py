from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    model_config = {
    "from_attributes": True
}

class TaskCreate(BaseModel):
    title: str
    description: str = None
    completed: bool = False

class TaskResponse(TaskCreate):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

