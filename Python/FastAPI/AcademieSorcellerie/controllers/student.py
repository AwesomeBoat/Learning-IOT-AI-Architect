from fastapi import APIRouter
from database import *
from models.student import *
router = APIRouter(
    prefix="/student",
    tags=["Student"]
)

# GET

@router.get("/get_student")
def get_student():
    return students

@router.get("/get_student/{student_id}")
def get_student_by_id(student_id : int) -> dict :
    """
    Return student's info by it's id
    """
    # check if exist
    student = find_student_or_404(student_id)

    return student


# POST

@router.post("/create_student", status_code=status.HTTP_201_CREATED)
def create_student(student_data : StudentCreate):
    new_student = {}

    # Generate id
    new_student["id"] = generate_id(students)

    # Fill rest of the data
    new_student.update(student_data.model_dump(exclude_unset=True))

    students.append(new_student)
    return new_student


# PUT

@router.put("/create_student/{student_id}", status_code=status.HTTP_200_OK)
def replace_student(student_id : int, replace_data : StudentCreate) -> dict:
    """
    Change every information about student
    """
    # Check if exists
    student = find_student_or_404(student_id)

    # replace data
    student.update(replace_data.model_dump())

    return student

@router.patch("/update_student/{student_id}")
def update_student(student_id : int, data : StudentUpdate) -> dict:

    # Check if exist
    student = find_student_or_404(student_id)

    # Replace data
    student.update(data.model_dump(exclude_unset=True))

    return student


# Delete

@router.delete("/delete_student/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int):

    # check if exist
    student = find_student_or_404(student_id)

    # delete
    students.remove(student)