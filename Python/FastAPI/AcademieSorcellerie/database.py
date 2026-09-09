from fastapi import HTTPException,status
from models.user import UserCreate

houses = [
    {
        "id": 1,
        "name": "Gryffondor",
        "color": "rouge et or",
        "founder": "Godric Gryffondor",
        "values": ["courage", "bravoure", "détermination"],
    },
    {
        "id": 2,
        "name": "Serpentard",
        "color": "vert et argent",
        "founder": "Salazar Serpentard",
        "values": ["ambition", "ruse", "leadership"],
    },
    {
        "id": 3,
        "name": "Poufsouffle",
        "color": "jaune et noir",
        "founder": "Helga Poufsouffle",
        "values": ["loyauté", "patience", "travail"],
    },
    {
        "id": 4,
        "name": "Serdaigle",
        "color": "bleu et bronze",
        "founder": "Rowena Serdaigle",
        "values": ["sagesse", "intelligence", "créativité"],
    },
]

students = [
    {"id": 1, "name": "Harry Potter", "year_of_study": 5, "house_id": 1, "pet": "Hedwige (chouette)", "status": "active"},
    {"id": 2, "name": "Hermione Granger", "year_of_study": 5, "house_id": 1, "pet": "Pattenrond (chat)", "status": "active"},
    {"id": 3, "name": "Ron Weasley", "year_of_study": 5, "house_id": 1, "pet": "Croûtard (rat)", "status": "active"},
    {"id": 4, "name": "Drago Malefoy", "year_of_study": 5, "house_id": 2, "pet": "aucun", "status": "active"},
    {"id": 5, "name": "Blaise Zabini", "year_of_study": 5, "house_id": 2, "pet": "aucun", "status": "active"},
    {"id": 6, "name": "Cédric Diggory", "year_of_study": 6, "house_id": 3, "pet": "aucun", "status": "graduated"},
    {"id": 7, "name": "Susan Bones", "year_of_study": 4, "house_id": 3, "pet": "chat", "status": "active"},
    {"id": 8, "name": "Luna Lovegood", "year_of_study": 4, "house_id": 4, "pet": "Lubulle (crapaud)", "status": "active"},
    {"id": 9, "name": "Cho Chang", "year_of_study": 6, "house_id": 4, "pet": "chouette", "status": "active"},
    {"id": 10, "name": "Neville Londubat", "year_of_study": 5, "house_id": 1, "pet": "Trevor (crapaud)", "status": "active"},
]

teachers = [
    {"id": 1, "name": "Minerva McGonagall", "subject": "Métamorphose", "seniority": 30},
    {"id": 2, "name": "Severus Rogue", "subject": "Potions", "seniority": 20},
    {"id": 3, "name": "Filius Flitwick", "subject": "Sortilèges", "seniority": 35},
    {"id": 4, "name": "Pomona Chourave", "subject": "Botanique", "seniority": 25},
    {"id": 5, "name": "Rubeus Hagrid", "subject": "Soins aux créatures magiques", "seniority": 15},
    {"id": 6, "name": "Remus Lupin", "subject": "Défense contre les forces du Mal", "seniority": 10},
]

subjects = [
    {"id": 1, "title": "Métamorphose", "prerequisite_level": "intermédiaire", "max_capacity": 20, "teacher_id": 1, "academic_year": 3},
    {"id": 2, "title": "Potions", "prerequisite_level": "débutant", "max_capacity": 25, "teacher_id": 2, "academic_year": 1},
    {"id": 3, "title": "Sortilèges", "prerequisite_level": "débutant", "max_capacity": 30, "teacher_id": 3, "academic_year": 1},
    {"id": 4, "title": "Botanique", "prerequisite_level": "intermédiaire", "max_capacity": 20, "teacher_id": 4, "academic_year": 2},
    {"id": 5, "title": "Soins aux créatures magiques", "prerequisite_level": "avancé", "max_capacity": 15, "teacher_id": 5, "academic_year": 4},
    {"id": 6, "title": "Défense contre les forces du Mal", "prerequisite_level": "avancé", "max_capacity": 20, "teacher_id": 6, "academic_year": 5},
]

users = [
    {"id": 1, "email": "admin@academie-sorcellerie.fr", "password": "admin123", "role": "admin", "student_id": None, "teacher_id": None},
    {"id": 2, "email": "harry.potter@academie-sorcellerie.fr", "password": "poudlard123", "role": "student", "student_id": 1, "teacher_id": None},
    {"id": 3, "email": "hermione.granger@academie-sorcellerie.fr", "password": "poudlard123", "role": "student", "student_id": 2, "teacher_id": None},
    {"id": 4, "email": "minerva.mcgonagall@academie-sorcellerie.fr", "password": "metamorphose123", "role": "teacher", "student_id": None, "teacher_id": 1},
    {"id": 5, "email": "severus.rogue@academie-sorcellerie.fr", "password": "potions123", "role": "teacher", "student_id": None, "teacher_id": 2},
]


def find_house_or_404(house_id : int) -> dict:

    for house in houses:
        if house["id"] == house_id:
            return house

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"error" : "house not found"}
    )


def find_teacher_or_404(teacher_id : int) -> dict:

    for teacher in teachers:
        if teacher["id"] == teacher_id:
            return teacher


    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"error" : "teacher not found"}
    )

def generate_id(list_name):
    """
    Generate a unique ordored id for a given data list
    return 404 if list doesn't exist
    """
    lists = [teachers,houses,students,subjects,users]

    if list_name in lists:
        if list_name :
            return max([element["id"] for element in list_name]) + 1
        else :
            return 1
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"error" : "List doesn't exists "}
    )

def find_student_or_404(student_id : int) -> dict :

    for student in students:
        if student["id"] == student_id:
            return student

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"error" : "Student not found"}
    )

def find_subject_or_404(subject_id : int) -> dict :

    for subject in subjects :
        if subject["id"] == subject_id:
            return subject

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"error" : "Subject not found"}
    )

def find_user_or_404(user_id:int)-> dict:
    for user in users:
            if user["id"] == user_id:
                return user
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"error" : "user not found"}
    )




def check_if_user_data_is_valid(data : dict | UserCreate):
    """
    Return 1 if data is valid.

    The data is valid when :
    - role : 
        - admin => teacher_id and student_id must be None
        - student => student_id must exist and teacher_id must be None
        - teacher => teacher_id must exist and student_id must be None

    Data =
    {
        email : str
        password : str
        role : Literal["student","teacher","admin"]
        student_id : int | None = None
        teacher_id : int | None = None
    }

    """
    # Transform the data in a dict if it's in the BaseModel Form
    if not isinstance(data, dict):
        data_to_check = data.model_dump()
    else:
        data_to_check = data

    if data_to_check["role"] == "student":
            # check if has a student_id

        if data_to_check["student_id"] is None:
            return 0
        
        # Check if student_id exists
        else :
            if not data_to_check["student_id"] in [student["id"] for student in students]:
                return 0

        # check if teacher_id is None
        if data_to_check["teacher_id"] is not None:
            return 0

    # Check for teacher role
    elif data_to_check["role"] == "teacher":

        # check if has teacher_id
        if data_to_check["teacher_id"] is None:
            return 0

        # Check if teacher id exists
        else:
            if not data_to_check["teacher_id"] in [teacher["id"] for teacher in teachers]:
                return 0

        
        # Check if student_id is None
        if data_to_check["student_id"] is not None:
            return 0

    # Check for admin role
    elif data_to_check["role"] == "admin":

        # check if teacher_id and student_id are None

        if data_to_check["student_id"] is not None or data_to_check["teacher_id"] is not None:
            return 0

    return 1