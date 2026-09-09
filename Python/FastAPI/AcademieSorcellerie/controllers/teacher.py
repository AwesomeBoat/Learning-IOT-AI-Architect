from fastapi import APIRouter
from database import *
from models.teacher import *

router = APIRouter(
    prefix="/teacher",
    tags=["Teacher"]
)


# GET

@router.get("/get_teacher")
def get_teacher():
    return teachers


@router.get("/get_teacher/{teacher_id}")
def get_teacher_by_id(teacher_id : int) -> dict:
    """
    Get teacher info by it's id 
    """
    # Check if exists
    return find_teacher_or_404(teacher_id)

# Post
@router.post("/create_teacher", status_code=status.HTTP_201_CREATED)
def create_teacher(teacher_data : TeacherCreate):
    """
    Create teacher
    """
    new_teacher = {}
    # Generate id
    teacher_id = generate_id(teachers)
    new_teacher["id"] = teacher_id

    # create teacher dict

    new_teacher.update(teacher_data.model_dump(exclude_unset=True))
    

    # Add to database
    teachers.append(new_teacher)

    return new_teacher

# PUT
@router.put("/replace_teacher/{teacher_id}", status_code=status.HTTP_200_OK)
def replace_teacher(teacher_id : int, teacher_data : TeacherCreate):

    # Check if exists
    teacher = find_teacher_or_404(teacher_id)

    # Replace
    teacher.update(teacher_data.model_dump())

    return teacher

# PATCH

@router.patch("/update_teacher/{teacher_id}", status_code=status.HTTP_200_OK)
def update_teacher(teacher_id : int, teacher_data : TeacherUpdate) -> dict:
    """
    Update teacher specifies values by it's id
    """
    # Check if exist
    teacher = find_teacher_or_404(teacher_id)

    # Update data
    teacher.update(teacher_data.model_dump(exclude_unset=True))

    return teacher
# DELETE

@router.delete("/delete_teacher/{teacher_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_teacher(teacher_id : int):
    """
    Remove a teacher by using it's id
    """
    # Check if exists
    teacher = find_teacher_or_404(teacher_id)

    # Delete
    teachers.remove(teacher)