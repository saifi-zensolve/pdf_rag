from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.jwt import create_access_token, get_current_user

router = APIRouter(prefix="/api/v1/auth")


@router.post("/token")
async def post_token(data: OAuth2PasswordRequestForm = Depends()) -> dict:
    token = create_access_token(data={"username": data.username})
    return {"token": token}


@router.get("/user")
async def get_user(user: dict = Depends(get_current_user)) -> dict:
    return {"user": user}
