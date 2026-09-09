from fastapi import APIRouter, status
from models.house import *
from database import *

router = APIRouter(
    prefix="/house",
    tags=["House"]
)



#  GET
@router.get("/get_house")
def get_houses():
    """
    Get houses infos
    """
    return houses

@router.get("/get_house/{house_id}")
def get_house_by_id(house_id : int):
    """
    Get one house infos by it's id
    """
    return find_house_or_404(house_id)

# Post
@router.post("/create_house", status_code=status.HTTP_201_CREATED)
def create_house(house_data : HouseCreate):
    """
    Create a new House
    """
    new_house = {}

    # Generate house id
    if houses:
        house_id = max([house["id"] for house in houses]) + 1
    else:
        house_id = 1
    # Add all data to house
    new_house["id"] = house_id
    new_house.update(house_data.model_dump())

    # Add to database
    houses.append(new_house)

    return new_house

# Patch
@router.patch("/update_house/{house_id}", status_code=status.HTTP_200_OK)
def update_house(house_id : int, data : HouseUpdate) -> dict:
    """
    Update specified fields for house
    """
    # Check if exist
    house = find_house_or_404(house_id)

    # Update data
    new_data = data.model_dump(exclude_unset=True)

    house.update(new_data)

    return house

# Delete
@router.delete("/delete_house/{house_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_house(house_id : int):
    """
    Delete house by it's id
    """

    # check if exists
    house = find_house_or_404(house_id)

    # Delete
    houses.remove(house)


