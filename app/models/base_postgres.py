from typing import Generic, Optional, Type, TypeVar
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from app.endpoints.db import Base

TableType = TypeVar("TableType", bound=Base)

class BasePostgres(Generic[TableType]):
    def __init__(self, model: Type[TableType]):
        """
        Base Model with CRUD.

        Parameters:
            model: A SQLAlchemy model class
            schema: A Pydantic model (schema) class
        """
        self.model = model


    async def get(self, db: AsyncSession, _id: str) -> Optional[TableType]:
        return await db.get(self.model, _id)

    async def get_by(self, db: AsyncSession, _filter: dict):
        query = select(self.model).filter_by(**_filter)
        result = await db.execute(query)
        return result.scalars().all()

    async def create(self, db: AsyncSession, obj_dict: dict):
        obj_db = self.model(**obj_dict)
        db.add(obj_db)
        await db.commit()
        await db.refresh(obj_db)
        return obj_db