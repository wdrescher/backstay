from fastapi import APIRouter

from api.models.requests import ResetEmailRequest
from api.models.responses import SuccessResponse
from api.services.email import reset_password

router = APIRouter( 
    prefix="/email", 
    tags=["Email"]
)

@router.post("/reset-password", response_model=SuccessResponse)
async def reset(request: ResetEmailRequest):
    await reset_password(request.email)
    return SuccessResponse()
