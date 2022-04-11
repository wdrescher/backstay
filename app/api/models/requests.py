from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

from datetime import datetime

class SignupRequest(BaseModel): 
    email: str
    password: str
    first_name: str
    last_name: str

class AccessRequest(BaseModel): 
    email: str
    password: str

class ResetPasswordRequest(BaseModel): 
    profile_id: str
    new_password: str

class ChangePasswordRequest(BaseModel): 
    password: str

class UpdateUserRequest(BaseModel):
    first_name: str
    last_name: str

class ResetEmailRequest(BaseModel):
    email: str