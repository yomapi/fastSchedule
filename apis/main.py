from fastapi import FastAPI, APIRouter
from v1.endpoints.router import v1_router

app = FastAPI()
router = APIRouter()


app.include_router(v1_router, tags=["v1"], prefix="/api/v1")
