from fastapi import APIRouter, Depends, HTTPException

from api.services import auth
from api.services.dependencies import get_current_user
from api.models.user import Profile
from api.models.requests import UpdateUserRequest

router = APIRouter( 
    prefix="/user", 
    tags=["User"]
)

@router.get("/")
async def get_current_user(current_user: Profile = Depends(get_current_user)):
    return current_user

@router.post("/edit", response_model=Profile)
async def edit_current_user_endpoint(request: UpdateUserRequest, current_user: Profile = Depends(get_current_user)):
    result = await auth.edit_current_user(request, current_user)
    if result is None: 
        raise HTTPException(status_code=400, detail="failed to update user")
    current_user.first_name = request.first_name
    current_user.last_name = request.last_name
    return current_user