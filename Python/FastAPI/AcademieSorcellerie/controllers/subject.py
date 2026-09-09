from fastapi import APIRouter
from database import *
from models.subject import *


router = APIRouter(
    prefix="/subject",
    tags=["Subject"]
)


# GET
@router.get("/get_subject")
def get_subject():
    """
    return all subjects
    """

    return subjects

@router.get("/get_subject/{subject_id}")
def get_subject_by_id(subject_id : int) -> dict:

    # check if exists
    subject = find_subject_or_404(subject_id)

    return subject


# POST

@router.post("/create_subject", status_code=status.HTTP_201_CREATED)
def create_subject(subject_data : SubjectCreate) -> dict:
    """
    Create a new subject
    """

    #Generate ID
    new_subject = {}
    new_subject["id"] = generate_id(subjects)

    # Rest of data
    new_subject.update(subject_data.model_dump())
    subjects.append(new_subject)

    return new_subject

# PUT
@router.put("/create_subject/{subject_id}", status_code=status.HTTP_200_OK)
def modify_subject(subject_id : int, new_data : SubjectCreate) -> dict:
    """
    Modify all data for a subject except id
    """
    # check if exists
    subject = find_subject_or_404(subject_id)

    # Replace all data
    new_subject = new_data.model_dump()
    subject.update(new_subject)

    return new_subject


# PATCH
@router.patch("/update_subject/{subject_id}", status_code=status.HTTP_202_ACCEPTED)
def update_subject(subject_id : int, new_data : SubjectUpdate) -> dict:

    # check if exist
    subject = find_subject_or_404(subject_id)

    # replace
    new_data_dict = new_data.model_dump(exclude_unset=True)
    subject.update(new_data_dict)

    return new_data_dict

# DELETE
@router.delete("/delete_subject/{subject_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_subject(subject_id : int):
    """
    delete subject by it's id

    """
    # check if exist
    subject_to_delete = find_subject_or_404(subject_id)

    # delete
    subjects.remove(subject_to_delete)