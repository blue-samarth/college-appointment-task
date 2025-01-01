
import datetime
import logging

from pydantic import BaseModel , Field 
from fastapi import HTTPException

from src import db


class Student(BaseModel):
    """
    It is a class that contains the student model
    """
    name : int
    email : str
    password : str
    enrollment_no : int = Field(default_factory=int)
    created_at : datetime.datetime = Field(default_factory=datetime.datetime.now)
    enrolled_courses : dict = {}

    @classmethod
    async def create_student(cls, student: BaseModel) -> dict:
        """
        It is a class method that creates a student
        param student: Student: student object
            {
            'name': str,
            'email': str,
            'password': str
            }
        returns: dict: student object
            {
            'name': str,
            'email': str,
            'password': str,
            'enrollment_no': int,
            'created_at': datetime.datetime
            }
        """
        try:
            student = await db['students'].insert_one(student.dict())
            return student.dict()
        except Exception as e:
            logging.error(f"Error in creating student: {e}")
            raise HTTPException(status_code=500, detail=f"Error in creating student: {e}")
    

    @staticmethod
    async def get_student(enrollment_no : int) -> dict:
        """
        It is a class method that gets a student
        param enrollment_no: int: enrollment number
        returns: dict: student object
            {
            'name': str,
            'email': str,
            'enrollment_no': int,
            'created_at': datetime.datetime
            }
        """
        try:
            student = await db['students'].find_one({"enrollment_no": enrollment_no})
            return student
        except Exception as e:
            logging.error(f"Error in getting student: {e}")
            raise HTTPException(status_code=500, detail=f"Error in getting student: {e}")
        

    @staticmethod
    async def get_all_students() -> list:
        """
        It is a class method that gets all students
        returns: list: list of student objects
            [
                {
                    'name': str,
                    'email': str,
                    'enrollment_no': int,
                    'created_at': datetime.datetime
                }
            ]
        """
        try:
            students = await db['students'].find().to_list(length=None)
            return students
        except Exception as e:
            logging.error(f"Error in getting all students: {e}")
            raise HTTPException(status_code=500, detail=f"Error in getting all students: {e}")
        
    @staticmethod
    async def delete_student(enrollment_no : int) -> dict:
        """
        It is a class method that deletes a student
        param enrollment_no: int: enrollment number
        returns: dict: student object
            {
            'name': str,
            'email': str,
            'enrollment_no': int,
            'created_at': datetime.datetime
            }
        """
        try:
            student = await db.students.delete_one({"enrollment_no": enrollment_no})
            return student
        except Exception as e:
            logging.error(f"Error in deleting student: {e}")
            raise HTTPException(status_code=500, detail=f"Error in deleting student: {e}")
        
    
    def __to_dict__(self) -> dict:
        """
        It is a method that converts student object to dictionary
        returns: dict: student object
            {
            'name': str,
            'email': str,
            'enrollment_no': int,
            'created_at': datetime.datetime
            }
        """
        return {
            'name': self.name,
            'email': self.email,
            'enrollment_no': self.enrollment_no,
            'created_at': self.created_at
        }