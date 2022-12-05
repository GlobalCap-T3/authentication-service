from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from .base_postgres import BasePostgres
from app.schema.user import UserCreate
from app.endpoints.db import User

class UserModel(BasePostgres[User]):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def __init__(self):
        self.model = User

    @classmethod
    def hash_password(cls, password):
        return cls.pwd_context.hash(password)

    @classmethod
    def verify_password(cls, password, hash_password):
        return cls.pwd_context.verify(password, hash_password)

    async def create_user(self, db: AsyncSession, obj: UserCreate):
        obj_dict = obj.dict()
        password = obj_dict.pop("password")
        obj_dict["hashed_password"] = self.hash_password(password)
        return await super().create(db, obj_dict)