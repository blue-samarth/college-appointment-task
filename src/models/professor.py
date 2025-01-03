import logging
import datetime

from bson import ObjectId

from pydantic import BaseModel , Field
from fastapi import HTTPException

from src import db
from src.models import student

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
                f"i" : {"status": "free", "student_id": None} for i in range(8, 18)
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
                try:
                    student.add_course(enrollemnt_no, slot, professor["name"])
                except Exception as e:
                    logging.error(f"Error in adding course to student: {e}")
                    raise HTTPException(status_code=500, detail=f"Error in adding course to student: {e}")
                await db["professors"].update_one({"_id": ObjectId(professor_id)}, {"$set": professor})
                return professor["time_slots"]
            return {}
        except Exception as e:
            logging.error(f"Error in updating slot: {e}")
            raise HTTPException(status_code=500, detail=f"Error in updating slot: {e}")
        
    @staticmethod
    async def cancel_booking(professor_id: str, slot: str) -> dict:
        """
        It is a static method that cancels a booking of a professor
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
                student_id = professor["time_slots"][slot]["student_id"]
                professor["time_slots"][slot]["status"] = "free"
                professor["time_slots"][slot]["student_id"] = None
                try:
                    student.delete_course(student_id, slot)
                except Exception as e:
                    logging.error(f"Error in deleting course of student: {e}")
                    raise HTTPException(status_code=500, detail=f"Error in deleting course of student: {e}")
                await db["professors"].update_one({"_id": ObjectId(professor_id)}, {"$set": professor})
                return professor["time_slots"]
            return {}
        
        except Exception as e:
            logging.error(f"Error in cancel booking: {e}")
            raise HTTPException(status_code=500, detail=f"Error in cancel booking: {e}")

    @staticmethod
    async def get_all_free_slots(professor_id: str) -> dict:
        """
        It is a static method that gets all free slots of a professor
        param professor_id: str: professor id
        returns: dict: free slots object
        { 'slots':
            {
            'slot': str
            }
        }
        """
        try:
            professor = await db["professors"].find_one({"_id": ObjectId(professor_id)})
            if professor:
                free_slots = {
                    slot: slot_data
                    for slot, slot_data in professor["time_slots"].items()
                    if slot_data["status"] == "free"
                }
                return free_slots
            return {}
        except Exception as e:
            logging.error(f"Error in getting all free slots: {e}")
            raise HTTPException(status_code=500, detail=f"Error in getting all free slots: {e}")
        
    @staticmethod
    async def get_all_booked_slots(professor_id: str) -> dict:
        """
        It is a static method that gets all booked slots of a professor
        param professor_id: str: professor id
        returns: dict: booked slots object
        { 'slots':
            {
            'slot': str
            }
        }
        """
        try:
            professor = await db["professors"].find_one({"_id": ObjectId(professor_id)})
            if professor:
                booked_slots = {
                    slot: slot_data
                    for slot, slot_data in professor["time_slots"].items()
                    if slot_data["status"] == "booked"
                }
                return booked_slots
            return {}
        except Exception as e:
            logging.error(f"Error in getting all booked slots: {e}")
            raise HTTPException(status_code=500, detail=f"Error in getting all booked slots: {e}")
        
    @staticmethod
    async def new_slots_for_the_day(professor_id : str) -> dict:
        """
        This method is used to create new slots for the day
        """
        professor = await db["professors"].find_one({"_id": ObjectId(professor_id)})
        if professor:
            professor["time_slots"] = {
                f"i" : {"status": "free", "student_id": None} for i in range(8, 18)
            }
            await db["professors"].update_one({"_id": ObjectId(professor_id)}, {"$set": professor})
            return professor["time_slots"]
        return {}
    
    