from db import database
from uuid import uuid4
from passlib.context import CryptContext

from api.services.dependencies import get_user_from_email
from api.models.requests import SignupRequest
from api.models.user import PrivateProfile, Profile

salt = "jibberish_that_you_would_never_ever_guess"

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password): 
    return password_context.verify(salt + plain_password, hashed_password)

def hash_password(plain_password):
    return password_context.hash(salt + plain_password)

@database.transaction()
async def create_user(request: SignupRequest): 
    bearer_token: str = uuid4().__str__()
    hashed_password = hash_password(request.password)
    async with database.connection(): 
        result = await database.execute(
            query="""
                CALL create_user(:token, :email, :password, :first_name, :last_name)
            """, 
            values={
                "token": bearer_token, 
                "email": request.email, 
                "password": hashed_password, 
                "first_name": request.first_name, 
                "last_name": request.last_name
            }
        )
    if result is None: 
        raise "User already exists"

    async with database.connection(): 
        token = await database.fetch_one(
            query="""
                SELECT * FROM token WHERE bearer=:token
            """, 
            values={
                "token":bearer_token
            }
        )
    if token is None: 
        raise "Token not found"
    return token


async def check_password(username: str, password: str): 
    profile = await get_user_from_email(username)
    if profile is None or not verify_password(password, profile.password): 
        return None
    return profile

async def change_password(current_user: Profile, password:str): 
    hashed_password = hash_password(password)
    async with database.connection(): 
        result = await database.execute(
            query="""
                UPDATE profile SET password = :password WHERE profile_id = :profile_id
            """,
            values={
                "profile_id": current_user.profile_id, 
                "password": hashed_password
            }
        )
    return result

async def edit_current_user(new_profile: Profile, current_user: Profile):
    async with database.connection(): 
        result = await database.execute(
            query="""
                UPDATE profile
                SET 
                    first_name=:first_name, 
                    last_name= :last_name
                WHERE profile_id = :profile_id
            """, 
            values={
                "first_name": new_profile.first_name, 
                "last_name": new_profile.last_name,
                "profile_id": current_user.profile_id
            }
        )
    return result