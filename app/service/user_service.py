from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from .base_postgres import BasePostgres
from app.schema import UserCreate, UserLogin
from app.models.model import Users

class UserService(BasePostgres[Users]):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    model = Users

    @classmethod
    def hash_password(cls, password):
        return cls.pwd_context.hash(password)

    @classmethod
    def verify_password(cls, password, hash_password):
        return cls.pwd_context.verify(password, hash_password)

    @classmethod
    async def create_user(cls, db: AsyncSession, obj: UserCreate):
        obj_dict = obj.dict()
        password = obj_dict.pop("password")
        obj_dict["hashed_password"] = cls.hash_password(password)
        return await super().create(db, obj_dict)

    @classmethod
    async def authenticate(cls, db: AsyncSession, obj: UserLogin):
        user = await super().get_one(db, {"email": obj.email})
        if not user or not cls.verify_password(obj.password, user.hashed_password):
            return None
        return user