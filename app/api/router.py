from logging import getLogger
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from .deps import get_db, get_current_user
from app.endpoints import endpoints
from app.service.user_service import UserService
from app.schema import Token, UserCreate, UserLogin, UserBase

logger = getLogger(f'uvicorn.{__name__}')
router = APIRouter()

@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=Token)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        logger.debug("[api] Attempting to create user with email %s.", user.email)
        await UserService.create_user(db, user)
    except IntegrityError:
        logger.debug("[api] Create user %s failed.", user.email)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already existed."
        )
    logger.debug("[api] Create user %s successful.", user.email)
    return {
        "access_token": endpoints.jwt.generate_access_token(sub=user.email),
        "token_type": "bearer"
    }

@router.post("/login", status_code=status.HTTP_200_OK, response_model=Token)
async def verify_user(form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    usr = UserLogin(email=form.username, password=form.password)
    logger.debug("[api] Attempting to login with %s.", usr.email)
    user = await UserService.authenticate(db, usr)
    if not user:
        logger.debug("[api] Authentication for %s failed.", usr.email)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Incorrect username or password.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    logger.debug("[api] Authentication for %s succeeded.", usr.email)
    return {
        "access_token": endpoints.jwt.generate_access_token(sub=user.email),
        "token_type": "bearer"
    }

@router.get("/user/me", status_code=status.HTTP_200_OK, response_model=UserBase)
async def current_user(current_user: UserBase = Depends(get_current_user)):
    return jsonable_encoder(current_user)