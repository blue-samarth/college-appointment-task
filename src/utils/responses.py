from typing import Any , Optional

from fastapi.responses import JSONResponse
from pydantic import BaseModel

class APIResponse(BaseModel):
    """
    API Response model
    """
    status: str
    message: str
    data: Optional[Any] = None
    status_code: int

    @classmethod
    def respond(cls , status_code : int , status : str , message : str , data : Optional[Any] = None , token : Optional[str] = None) -> JSONResponse:
        """
        Function to return a JSONResponse object.
        Args:
            status_code (int): Status code to be returned.
            status (str): Status of the response.
            message (str): Message to be displayed.
            data (Any): Data to be returned.
        """
        return JSONResponse(
            status_code = status_code,
            content = {
                "status": status,
                "message": message,
                "token" : token,
                "data": data
            }
        )