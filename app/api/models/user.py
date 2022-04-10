from typing import Optional, List

from pydantic import BaseModel

class Profile(BaseModel): 
    profile_id: int
    email: str
    phone_number: Optional[str]
    first_name: str
    last_name: str

class PrivateProfile(Profile): 
    password: str
    token_id: str