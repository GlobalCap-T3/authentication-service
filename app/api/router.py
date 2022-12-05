from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from .deps import get_db
from app.models import crud_user_model
from app.schema.user import UserCreate
from app.schema.resp import ErrorResp, UserCreateResp

router = APIRouter()

@router.post(
    "/signup",
    status_code=201,
    responses={
        201: { "model": UserCreateResp },
        409: { "model": ErrorResp }
    }
)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        resp = await crud_user_model.create_user(db, user)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Email already existed.")
    return resp.__dict__
