import logging
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status , Request
from fastapi.responses import JSONResponse

from src import app 
from src.models.student import Student
from src.utils.responses import APIResponse
from src.utils.password_handle import PasswordHandle

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
        return APIResponse(status="success", message="Student created successfully")
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
        if not student:
            raise HTTPException(status_code=400, detail="Student does not exist")
        if not PasswordHandle().verify_password(password, student['password']):
            raise HTTPException(status_code=400, detail="Invalid password")
        return APIResponse(status="success", message="Student logged in successfully")
    except Exception as e:
        logging.error(f"Error in getting student: {e}")
        raise HTTPException(status_code=500, detail=f"Error in getting student: {e}")
    

@router.get("/get_student" , response_model=APIResponse)
async def get_student(request: Request) -> APIResponse:
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
        student = await Student.get_student(enrollment_no)
        return APIResponse(status="success", message=student)
    except Exception as e:
        logging.error(f"Error in getting student: {e}")
        raise HTTPException(status_code=500, detail=f"Error in getting student: {e}")