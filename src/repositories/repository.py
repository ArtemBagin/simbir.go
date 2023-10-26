from fastapi import HTTPException
from sqlalchemy import select, update

from database.database import async_session


class SQLAlchemyRepository:
    model = None
    no_data_error = HTTPException(
        status_code=403,
        detail="Invalid request, no such data exists.",
    )

    async def add_one(self, data: dict) -> int:
        async with async_session() as session:
            res = self.model(**data)
            session.add(res)
            await session.commit()
            return res

    async def edit_one(self, id: int, data: dict) -> int:
        async with async_session() as session:
            stmt = update(self.model).values(**data).filter_by(id=id).returning(self.model.id)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    async def find_all(self):
        async with async_session() as session:
            stmt = select(self.model)
            res = await session.execute(stmt)
            res = res.scalars().all()
            return res

    async def find_one(self, **filter_by):
        async with async_session() as session:
            stmt = select(self.model).filter_by(**filter_by)
            res = await session.execute(stmt)
            res = res.first()
            if not res:
                raise self.no_data_error
            return res[0]

    async def find(self, **filter_by):
        async with async_session() as session:
            stmt = select(self.model).filter_by(**filter_by)
            res = await session.execute(stmt)
            res = res.scalars().all()
            return res

    async def delete_one(self, **filter_by):
        async with async_session() as session:
            stmt = select(self.model).filter_by(**filter_by)
            res = await session.execute(stmt)
            res = res.first()
            if not res:
                raise self.no_data_error
            await session.delete(res[0])
            await session.commit()

    @staticmethod
    async def save_models(self, *args):
        async with async_session() as session:
            for arg in args:
                session.add(arg)
            await session.commit()
