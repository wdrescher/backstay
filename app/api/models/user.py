import enum
from typing import Optional, List

from pydantic import BaseModel

class Role(enum.Enum):
    ROWER = "ROWER"
    COACH = "COACH"
    EBOARD = "EBOARD"

class Profile(BaseModel): 
    profile_id: int
    email: str
    phone_number: Optional[str]
    first_name: str
    last_name: str
    role: Role

class PrivateProfile(Profile): 
    password: str
    token_id: str