from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from app.endpoints import endpoints
from app.service.user_service import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/auth/login")

async def get_db():
    async_session = endpoints.postgres.session()
    try:
        yield async_session
    finally:
        await async_session.close()

async def get_current_user(db = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = endpoints.jwt.verify_token(token)
    except JWTError:
        raise credentials_exception
    if not payload:
        raise credentials_exception

    username = payload.get("sub")
    user = await UserService.get_one(db, {"email": username})
    if user is None:
        raise credentials_exception
    return user