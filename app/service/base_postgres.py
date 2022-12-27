from typing import Generic, Optional, Type, TypeVar
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.model import Base

TableType = TypeVar("TableType", bound=Base)

class BasePostgres(Generic[TableType]):
    model: Type[TableType]

    @classmethod
    async def get(cls, db: AsyncSession, _id: str) -> Optional[TableType]:
        return await db.get(cls.model, _id)

    @classmethod
    async def get_one(cls, db: AsyncSession, _filter: dict):
        query = select(cls.model).filter_by(**_filter)
        result = await db.execute(query)
        return result.scalars().first()

    @classmethod
    async def get_list(cls, db: AsyncSession, _filter: dict):
        query = select(cls.model).filter_by(**_filter)
        result = await db.execute(query)
        return result.scalars().all()

    @classmethod
    async def create(cls, db: AsyncSession, obj_dict: dict):
        obj_db = cls.model(**obj_dict)
        db.add(obj_db)
        await db.commit()
        await db.refresh(obj_db)
        return obj_db