import logging
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status , Request
from fastapi.responses import JSONResponse

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
        return APIResponse(status="success", message="Student created successfully" , data = student)
    except Exception as e:
        logging.error(f"Error in creating student: {e}")
        raise HTTPException(status_code=500, detail=f"Error in creating student: {e}")
    

@router.get("/login_student" , response_model=APIResponse)
async def login_student(request: Request) -> APIResponse:
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
        enrollment_no : int = request.query_params['enrollment_no']
        password : str = request.query_params['password']
        student = await Student.get_student(enrollment_no)
        token = Token(user_id=student['enrollment_no'] , exp=datetime.now() , role="student").generate_token()
        if not student:
            raise HTTPException(status_code=400, detail="Student does not exist")
        if not PasswordHandle().verify_password(password, student['password']):
            raise HTTPException(status_code=400, detail="Invalid password")
        return APIResponse(status="success", message="Student logged in successfully" , data = student , token = token)
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
        return APIResponse(status="success", message="Professor created successfully")
    except Exception as e:
        logging.error(f"Error in creating professor: {e}")
        raise HTTPException(status_code=500, detail=f"Error in creating professor: {e}")
    

@router.get("/login_prof" , response_model=APIResponse)
async def login_prof(request: Request) -> APIResponse:
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
        email : str = request.query_params['email']
        password : str = request.query_params['password']
        professor = await Professor.get_professor(email)
        token = Token(user_id=professor['email'] , exp=datetime.now() , role="professor").generate_token()
        if not professor:
            raise HTTPException(status_code=400, detail="Professor does not exist")
        if not PasswordHandle().verify_password(password, professor['password']):
            raise HTTPException(status_code=400, detail="Invalid password")
        return APIResponse(status="success", message="Professor logged in successfully" , data = professor , token = token)
    except Exception as e:
        logging.error(f"Error in getting professor: {e}")
        raise HTTPException(status_code=500, detail=f"Error in getting professor: {e}")