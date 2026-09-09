from pydantic import BaseModel

class House(BaseModel):
    id :int 
    name : str
    color : str 
    founder : str 
    values : list

class HouseUpdate(BaseModel):
    name : str | None = None
    color : str | None = None
    values : list | None = None

class HouseCreate(BaseModel):
    name : str
    color : str 
    founder : str 
    values : list