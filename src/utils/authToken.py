import logging
from datetime import datetime , timedelta

from fastapi import Request 
import jwt
from pydantic import BaseModel

from src import SECRET_KEY

class AuthUser(BaseModel):
    user_id : str
    exp : int
    role : str


class Token():
    """
    It is a class to generate and verify tokens.
    """

    def __init__(self , user_id : str , role: str , exp : int = 60):
        """
        Constructor for baseToken class.
        Args:
            user_id (str): User ID.
            exp (datetime): Expiry time.
        """
        self.user_id = user_id
        self.exp = exp
        self.role = role
    

    def generate_token(self) -> str:
        """
        Function to generate token.
        Returns:
            str: Token.
        """
        expire : datetime = datetime.now() + timedelta(self.exp)
        token = jwt.encode({"user_id": self.user_id , "exp": expire , "role": self.role} ,
                            SECRET_KEY , algorithm="HS256")
        return token


    def decode_token(self , token : str) -> dict:
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
            return {"error": "Token is missing"}
        if token.startswith("Bearer "):
            token = token.split("Bearer ")[1]
        try:
            payload : dict = jwt.decode(token , SECRET_KEY , algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            logging.error("Token has expired")
            return {"error": "Token has expired"}
        except jwt.InvalidTokenError:
            logging.error("Invalid token")
            return {"error": "Invalid token"}
        except Exception as e:
            logging.error(f"Error in decoding token: {e}")
            return {"error": f"Error in decoding token: {e}"}
