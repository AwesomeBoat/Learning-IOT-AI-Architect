from pydantic import BaseModel, Field
from typing import Literal

class Student(BaseModel):
    id : int
    name : str
    year_of_study : int = Field(ge=1, le=7) # ge = Greater than or Equal, le = Less than or equal
    house_id : int
    pet : str
    status : Literal["active","graduated","fired"]


class StudentUpdate(BaseModel):
    name : str | None = None
    year_of_study : int | None = Field(default = None, ge=1, le=7)
    house_id : int | None = None
    pet : str | None = None
    status : Literal["active","graduated","fired"] | None = None

class StudentCreate(BaseModel):
    name : str
    year_of_study : int = Field(ge=1, le=7) 
    house_id : int
    pet : str
    status : Literal["active","graduated","fired"]
    