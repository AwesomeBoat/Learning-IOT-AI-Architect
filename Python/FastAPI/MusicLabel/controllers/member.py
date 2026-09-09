from fastapi import APIRouter, HTTPException, status
from database import *
from models.member import MemberCreate, MemberUpdate

router = APIRouter(
    prefix="/members",
    tags=["Member"]
)


# Get

@router.get("/get_members")
def get_members(role : str | None = None):
    result = members
    if role is not None:
        result = [member for member in members if member["role"].lower() == role.lower()]
    return result

@router.get("/get_members/{member_id}")
def get_member(member_id : int):
    result = members
    for member in result:
        if member["id"] == member_id:
            return member

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"error":"Artist not found"}
    )



# post

@router.post("/create_member",status_code=status.HTTP_201_CREATED)
def create_member(member_data : MemberCreate):
    """
    Créer un nouveau membre si l'artiste existe
    artist_id : int
    name : str
    role : str
    """
    # Create a new ID
    member_id = max([member["id"] for member in members]) + 1


    # Check if Artist id exists
    find_artist_or_404(member_data.artist_id)


    # Add the new member to the list
    member = {}
    member["id"] = member_id
    member.update(member_data.model_dump())
    

    members.append(member)

# patch
@router.patch("/update_member/{member_id}",status_code=status.HTTP_200_OK)
def update_member(member_id : int, member_update_data : MemberUpdate):

    # Check if member exist
    member = find_member_or_404(member_id)

    # check if artist group exists
    find_artist_or_404(member_update_data.artist_id)

    member_data = member_update_data.model_dump(exclude_unset=True)
    member.update(member_data)

@router.delete("/delete_member/{member_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_member(member_id : int):
    """
    Supprimer un member
    """
    # check if exist
    member = find_member_or_404(member_id)

    # delete
    members.remove(member)

