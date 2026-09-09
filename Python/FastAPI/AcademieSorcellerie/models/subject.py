from pydantic import BaseModel

class Subject(BaseModel):
    id : int
    title : str
    prerequisite_level : str
    max_capacity : int
    teacher_id : int
    academic_year : int


class SubjectUpdate(BaseModel):
    title : str | None = None
    prerequisite_level : str | None = None
    max_capacity : int | None = None
    teacher_id : int | None = None
    academic_year : int | None = None


class SubjectCreate(BaseModel):
    title : str
    prerequisite_level : str
    max_capacity : int
    teacher_id : int
    academic_year : int