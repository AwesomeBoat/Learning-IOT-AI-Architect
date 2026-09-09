from fastapi import APIRouter
from database import *
from models.user import *
from models.login import *

router = APIRouter(
    prefix="/user",
    tags=["User"]
)


# GET

@router.get("/get_user")
def get_all_user() :
    """
    Return all users
    """
    return users

@router.get("/get_user/{user_id}")
def get_user_by_id(user_id : int) -> dict:

    """
    Get user infos by it's id

    user_id : int
    """
    return find_user_or_404(user_id)
    

# Post
@router.post("/create_user", status_code=status.HTTP_201_CREATED)
def create_user(user_data : UserCreate) -> dict :
    """
    Create a new user
    """
    # Error handler

    if check_if_user_data_is_valid(user_data):

        # CHECK ALL PASSED, Let's create the user
        new_user = {}

        # Generate ID
        new_user["id"] = generate_id(users)

        # Fill rest of data
        new_user.update(user_data.model_dump())

        # add to the database
        users.append(new_user)
        return new_user
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error" : "User is not valid"}
        )


# Login
@router.post("/login")
def login(credentials : Login) -> dict:
    if email in [user["email"] for user in users]:
        user = [user for user in users if user["email"] == email]
        user = user[0]
        if password == user["password"]:

            # Return for Admin
            if user["role"] == "admin":
                return {"role" :user["role"],
                    }

            # return for teacher
            if user["role"] == "teacher":
                return {"role" : user["role"],
                        "teacher_id": user["teacher_id"]}

            if user["role"] == "student":
                return {"role" : user["role"],
                        "student_id" : user["student_id"]}

        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"error" : "Email or password is incorrect"}
            )
    else :
        raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail={"error" : "Email or password is incorrect"}
                    )
    

# PUT
@router.put("/create_user/{user_id}", status_code=status.HTTP_200_OK)
def modify_user(user_id : int, user_data : UserCreate) -> dict:
    """
    Modify all data of a user except it's id
    """
    # Check if exist
    user = find_user_or_404(user_id)

    # check if data is valid
    if check_if_user_data_is_valid(user_data):

        # Update with new data
        user.update(user_data.model_dump())

        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error" : "User_data is not valid"}
        )

# PATCH
@router.patch("/update_user/{user_id}", status_code=status.HTTP_200_OK)
def update_user(user_id : int, data : UserUpdate) -> dict:

    # Check if user exist
    user = find_user_or_404(user_id)

    # if student_id or teacher_id are not in data, set them to None
    # if email, password , role are not in data, keep them as they are in user
    # => This allow us to send the data with no missing keys so it can pass the valid test
    # => Because PATCH allow to send data with missing keys
    dump_data = {**user, **data.model_dump(exclude_unset=True)}


    
    # Check if data is valid
    if check_if_user_data_is_valid(dump_data) :

        # Update
        user.update(dump_data)

        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error" : "data is not valid"}
        )

# DELETE
@router.delete("/delete_user", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id : int):

    # Check if exist
    user_to_del = find_user_or_404(user_id)

    # Delete
    users.remove(user_to_del)

