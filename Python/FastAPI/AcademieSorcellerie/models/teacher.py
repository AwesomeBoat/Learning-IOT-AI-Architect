from pydantic import BaseModel

class Teacher(BaseModel):
    id : int
    name : str
    subject : str
    seniority : int

class TeacherUpdate(BaseModel):
    name : str | None = None
    subject : str | None = None
    seniority : int | None = None

class TeacherCreate(BaseModel):
    name : str
    subject : str
    seniority : int