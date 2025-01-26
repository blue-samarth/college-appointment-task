
import datetime
import logging
from typing import Dict, Optional

from pydantic import BaseModel , Field 
from fastapi import HTTPException

from src import db


class Student(BaseModel):
    """
    It is a class that contains the student model
    """
    name : str
    email : str
    password : str
    enrollment_no : Optional[int] = Field(default_factory=int)
    created_at : datetime.datetime = Field(default_factory=datetime.datetime.now)
    enrolled_courses: Optional[Dict[str, str]] = Field(default_factory=dict)

    @classmethod
    async def create_student(cls , student : BaseModel) -> dict:
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
            stud = await db['students'].find_one({"email": student.email})
            if stud:
                raise HTTPException(status_code=400, detail="Student already exists")
            total_students = await db['students'].count_documents({})
            if not total_students:
                enrollment_no : int = 1
            else:
                last_student : dict = await db['students'].find_one(sort=[("enrollment_no", -1)])
                enrollment_no = last_student['enrollment_no'] + 1
            student_data = student.model_dump()  # or student.dict() for older Pydantic versions
            student_data.update({
                'enrollment_no': enrollment_no,
                'created_at': datetime.datetime.now(),
                'enrolled_courses': {}
            })
            result = await db['students'].insert_one(student_data)

            inserted_student = await db['students'].find_one({"_id" : result.inserted_id})
            inserted_student['_id'] = str(inserted_student['_id'])

            return inserted_student

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
    async def add_course(enrollment_no : int , time_slot : int , prof_name : str):
        """
        It is a class method that adds a course to a student
        param enrollment_no: int: enrollment number
        param time_slot: int: time slot
        param prof_name: str: professor name
        """
        try:
            student = await db['students'].find_one({"enrollment_no": enrollment_no})
            if student:
                student['enrolled_courses'][time_slot] = prof_name
                await db['students'].update_one({"enrollment_no": enrollment_no}, {"$set": student})
            else:
                raise HTTPException(status_code=404, detail="Student not found")
        except Exception as e:
            logging.error(f"Error in adding course: {e}")
            raise HTTPException(status_code=500, detail=f"Error in adding course: {e}")
        
    
    @staticmethod
    async def delete_course(enrollment_no : int , time_slot : int):
        """
        It is a class method that deletes a course of a student
        """
        try:
            student = await db['students'].find_one({"enrollment_no": enrollment_no})
            if student:
                student['enrolled_courses'].pop(time_slot)
                await db['students'].update_one({"enrollment_no": enrollment_no}, {"$set": student})
            else:
                raise HTTPException(status_code=404, detail="Student not found")
        except Exception as e:
            logging.error(f"Error in deleting course: {e}")
            raise HTTPException(status_code=500, detail=f"Error in deleting course: {e}")


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