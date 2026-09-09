from fastapi import FastAPI
from controllers import house, teacher, student ,subject, user
from database import *
import uvicorn

app = FastAPI(
    title="Wizard Academy API",
    version="1.0"
)

app.include_router(house.router)
app.include_router(teacher.router)
app.include_router(student.router)
app.include_router(subject.router)
app.include_router(user.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
