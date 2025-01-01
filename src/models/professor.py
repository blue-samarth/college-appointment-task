import logging
import datetime

from bson import ObjectId

from pydantic import BaseModel , Field
from fastapi import HTTPException

from src import db

class Professor(BaseModel):
    """
    It is a pydanitc class that contains the professor model
    """
    id : str = Field(default_factory=str)
    name : str
    email : str
    password : str
    time_slots : dict
    created_at : datetime.datetime = Field(default_factory=datetime.datetime.now)

    @classmethod
    async def create_professor(cls, professor: BaseModel) -> dict:
        """
        It is a class method that creates a professor
        param professor: BaseModel: professor object
            {
            'name': str,
            'email': str,
            'password': str
            }
        returns: dict: professor object
            {
            'name': str,
            'email': str,
            'time_slots': dict,
            'created_at': datetime.datetime
            }
        """
        try:
            time_slots = {
                f"{i}-{j}": {"status": "free", "student_id": None}
                for i in range(7) for j in range(8, 18)
            }
            professor_data = professor.dict()
            professor_data['time_slots'] = time_slots
            result = await db["professors"].insert_one(professor_data)
            inserted_professor = await db["professors"].find_one({"_id": result.inserted_id})
            if inserted_professor:
                inserted_professor["_id"] = str(inserted_professor["_id"])
            return inserted_professor
        except Exception as e:
            logging.error(f"Error in creating professor: {e}")
            raise HTTPException(status_code=500, detail=f"Error in creating professor: {e}")
        
    @staticmethod
    async def get_slot(professor_id: str) -> dict:
        """
        It is a static method that gets a slot of a professor
        param professor_id: str: professor id
        param slot: str: slot
        returns: dict: slot object
        { 'slot':
            {
            'status': str,
            'student_id': str
            }
        }
        """
        try:
            professor = await db["professors"].find_one({"_id": ObjectId(professor_id)})
            if professor:
                return professor["time_slots"]
            return {}
        except Exception as e:
            logging.error(f"Error in getting slot: {e}")
            raise HTTPException(status_code=500, detail=f"Error in getting slot: {e}")
        
    @staticmethod
    async def update_slot(professor_id: str, slot: str, enrollemnt_no : int) -> dict:
        """
        It is a static method that updates a slot of a professor
        param professor_id: str: professor id
        param slot: str: slot
        param student_id: str: student id
        returns: dict: slot object
        { 'slot':
            {
            'status': str,
            'student_id': str
            }
        }
        """
        try:
            professor = await db["professors"].find_one({"_id": ObjectId(professor_id)})
            if professor:
                professor["time_slots"][slot]["status"] = "booked"
                professor["time_slots"][slot]["student_id"] = enrollemnt_no
                await db["professors"].update_one({"_id": ObjectId(professor_id)}, {"$set": professor})
                return professor["time_slots"]
            return {}
        except Exception as e:
            logging.error(f"Error in updating slot: {e}")
            raise HTTPException(status_code=500, detail=f"Error in updating slot: {e}")
        
    
