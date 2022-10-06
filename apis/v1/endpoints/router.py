from fastapi import APIRouter
from v1.endpoints.schedules import router as schedules_router

v1_router = APIRouter()
v1_router.include_router(
    schedules_router,
    tags=["schedule"],
    prefix="/schedule",
)
