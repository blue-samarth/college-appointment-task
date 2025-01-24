import logging
from datetime import datetime , timedelta

from fastapi import Request 
import jwt
from pydantic import BaseModel

from src import SECRET_KEY
from src.utils.exception import MinorException


class Token(BaseModel):
    """
    It is a class to generate and verify tokens.
    """
    user_id : str
    exp : int = 60
    role : str

    @classmethod
    def create_token(cls) -> str:
        """
        Constructor for baseToken class.
        Args:
            user_id : str: User ID.
            exp : datetime: Expiry time.
            role : str : Role.
        """
        print(11)
        print(cls.model_dump())
        exp = datetime.now() + timedelta(minutes=cls.exp)
        print(12)
        token_data = cls.model_dump()
        print(13)
        token = jwt.encode(token_data, SECRET_KEY, algorithm="HS256")
        print(14)
        return token

    @staticmethod
    def decode_token(token : str) -> dict:
        """
        Function to decode token.
        Args:
            token (str): Token.
        Returns:
            dict: Decoded token.
        """
        if not token: 
            logging.error("Token is missing")
            return {"error": "Token is missing"}
        try:
            return jwt.decode(token , SECRET_KEY , algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            logging.error("Token has expired")
            return {"error": "Token has expired"}
        except jwt.InvalidTokenError:
            logging.error("Invalid token")
            return {"error": "Invalid token"}
        
    
    def decode_token_from_header(self , request : Request) -> dict:
        """
        Function to decode token from header.
        Args:
            request (Request): Request object.
        Returns:
            dict: Decoded token.
        """
        token : str = request.headers.get("Authorization")
        if not token: 
            logging.error("Token is missing")
            raise MinorException(status_code=401, message="Token is missing")
        if token.startswith("Bearer "):
            token = token.split("Bearer ")[1]
        try:
            payload : dict = jwt.decode(token , SECRET_KEY , algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            logging.error("Token has expired")
            raise MinorException(status_code=401, message="Token has expired")
        except jwt.InvalidTokenError:
            logging.error("Invalid token")
            raise MinorException(status_code=401, message="Token is invalid")
        except Exception as e:
            logging.error(f"Error in decoding token: {e}")
            raise MinorException(status_code=401, message="Error in decoding token")
