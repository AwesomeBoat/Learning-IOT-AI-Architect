from pydantic import BaseModel
from typing import Literal

class User(BaseModel):
    id : int
    email : str
    password : str
    role : Literal["student","teacher","admin"]
    student_id : int | None = None
    teacher_id : int | None = None


class UserUpdate(BaseModel):
    email : str | None = None
    password : str | None = None
    role : Literal["student","teacher","admin"] | None = None
    student_id : int | None = None
    teacher_id : int | None = None

class UserCreate(BaseModel):
    email : str
    password : str
    role : Literal["student","teacher","admin"]
    student_id : int | None = None
    teacher_id : int | None = None