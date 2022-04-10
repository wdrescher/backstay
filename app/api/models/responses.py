from pydantic import BaseModel
from datetime import date, datetime
from typing import List

from api.models.user import Profile

class TokenResponse(BaseModel): 
    bearer: str
    expiration_date: date

class LoginResponse(BaseModel): 
    profile: Profile
    token: str

class SuccessResponse(BaseModel):
    """
    api -> client
    """

    status = 'ok'    
