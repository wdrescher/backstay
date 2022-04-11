from fastapi import APIRouter

from api.routes import auth, user, email

router = APIRouter()

router.include_router(auth.router)
router.include_router(user.router)
router.include_router(email.router)