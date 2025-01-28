import logging
from typing import Callable , Any , TypeVar , Dict
from functools import wraps

from fastapi import Request , HTTPException

from src.utils.authToken import Token
from src.utils.exception import MinorException

T = TypeVar("T")

def accept_payload(func : Callable[... , T]) -> Callable[... , T]:
    @wraps(func)
    async def wrapper(request : Request , *args : Any , **kwargs : Any) -> T:
        try:
            payload : dict = Token.decode_token_from_header(request.headers['Authorization'])
            return await func(request , payload , *args , **kwargs)
        except MinorException as e:
            logging.error(f"Error in accepting payload: {e}")
            raise HTTPException(status_code=401 , detail=str(e))
                
        except Exception as e:
            logging.error(f"Error in accepting payload: {e}")
            raise HTTPException(status_code=500 , detail=str(e))
    return wrapper

# working
# @accept_payload
# xyz(request : Request , payload : dict) -> dict:


def verify_payload(role: str) -> Callable[..., T]:
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(request: Request, payload: Dict, *args: Any, **kwargs: Any) -> T:
            try:
                if payload.get('role') == role:
                    return await func(request, payload, *args, **kwargs)
                
                raise MinorException("Unauthorized access")
            
            except MinorException as e:
                logging.error(f"Error in verifying payload: {e}")
                raise HTTPException(status_code=403, detail=str(e))
            
            except Exception as e:
                logging.error(f"Error in verifying payload: {e}")
                raise HTTPException(status_code=500, detail=str(e))
            
        return wrapper
    return decorator

# working
# @accept_payload
# @verify_payload("admin")
# xyz(request : Request , payload : dict) -> dict:
