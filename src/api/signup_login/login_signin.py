import logging
from datetime import datetime

from fastapi import APIRouter, HTTPException, Request , Body

from src.models.student import Student
from src.models.professor import Professor
from src.utils.responses import APIResponse
from src.utils.password_handle import PasswordHandle
from src.utils.authToken import Token

router = APIRouter()

# @router.post("/login" , response_model=APIResponse)
# async def login(request: Request, username: str, password: str):


@router.post("/signup_student" , response_model=APIResponse)
async def signup(student: Student) -> APIResponse:
    """
    It is a route that creates a student
    param student: Student: student object
        {
        'name': str,
        'email': str,
        'password': str
        }
    returns: APIResponse: APIResponse object
        {
        'status': str,
        'message': str
        }
    """
    try:
        student.password = PasswordHandle().get_password_hash(student.password)
        student = await Student.create_student(student)
        return APIResponse(
            status="success", 
            status_code=200,
            message="Student created successfully" , 
            data = student)
    except Exception as e:
        logging.error(f"Error in creating student: {e}")
        raise HTTPException(status_code=500, detail=f"Error in creating student: {e}")

    

@router.post("/login_student" , response_model=APIResponse)
async def login_student(
    enrollment_no : int = Body(...),
    password : str = Body(...)
) -> APIResponse:
    """
    It is a route that gets a student
    param enrollment_no: int: enrollment number
    returns: APIResponse: APIResponse object
        {
        'status': str,
        'message': str
        }
    """
    try:
        student = await Student.get_student(int(enrollment_no))

        if not student:
            raise HTTPException(status_code=400, detail="Student does not exist")

        if not PasswordHandle().verify_password(password, student['password']):
            raise HTTPException(status_code=400, detail="Invalid password")
        
        token = Token(user_id=str(student['enrollment_no']) , exp=60 , role="student").create_token()

        student['_id'] = str(student['_id'])
        return APIResponse(status="success", status_code =200, 
                           message="Student logged in successfully" , 
                           data = student , token = token)
    except Exception as e:
        logging.error(f"Error in getting student: {e}")
        raise HTTPException(status_code=500, detail=f"Error in getting student: {e}")
    

@router.post("/signup_prof" , response_model=APIResponse)
async def signup_prof(professor: Professor) -> APIResponse:
    """
    It is a route that creates a professor
    param professor: Professor: professor object
        {
        'name': str,
        'email': str,
        'password': str
        }
    returns: APIResponse: APIResponse object
        {
        'status': str,
        'message': str
        }
    """
    try:
        professor.password = PasswordHandle().get_password_hash(professor.password)
        professor = await Professor.create_professor(professor)
        return APIResponse(
            status="success", 
            status_code=201,
            message="Professor created successfully",
            data = professor
            )
    except Exception as e:
        logging.error(f"Error in creating professor: {e}")
        raise HTTPException(status_code=500, detail=f"Error in creating professor: {e}")
    

@router.post("/login_prof" , response_model=APIResponse)
async def login_prof(
    email : str = Body(...),
    password : str = Body(...)
) -> APIResponse:
    """
    It is a route that gets a professor
    param email: str: email
    param password: str: password
    returns: APIResponse: APIResponse object
        {
        'status': str,
        'message': str
        }
    """
    try:
        professor = await Professor.get_professor_by_email(email)
        token = Token(user_id=professor['email'] , exp=60 , role="professor").create_token()
        professor['_id'] = str(professor['_id'])
        if not professor:
            raise HTTPException(status_code=400, detail="Professor does not exist")
        if not PasswordHandle().verify_password(password, professor['password']):
            raise HTTPException(status_code=400, detail="Invalid password")
        return APIResponse(status="success", 
                           status_code= 200,
                           message="Professor logged in successfully" , 
                           data = professor , token = token)
    except Exception as e:
        logging.error(f"Error in getting professor: {e}")
        raise HTTPException(status_code=500, detail=f"Error in getting professor: {e}")