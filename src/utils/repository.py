from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession


class SQLAlchemyRepository:
    model = None
    no_data_error = HTTPException(
        status_code=404,
        detail="Invalid request, no such data exists.",
    )

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: dict) -> int:
        res = self.model(**data)
        self.session.add(res)
        await self.session.commit()
        return res

    async def edit_one(self, id: int, data: dict) -> int:
        stmt = update(self.model).values(**data).filter_by(id=id).returning(self.model.id)
        res = await self.session.execute(stmt)
        await self.session.commit()
        return res.scalar_one()

    async def find_all(self):
        stmt = select(self.model)
        res = await self.session.execute(stmt)
        res = res.scalars().all()
        res = [row.to_read_model() for row in res]
        return res

    async def find_one(self, error=False, raw=False, **filter_by):
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        res = res.first()
        if error:
            return res
        if not res:
            raise self.no_data_error
        if raw:
            return res[0]
        res = res[0].to_read_model()
        return res

    async def find(self, **filter_by):
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        res = res.scalars().all()
        res = [row.to_read_model() for row in res]
        return res

    async def delete_one(self, **filter_by):
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        res = res.first()
        if not res:
            raise self.no_data_error
        await self.session.delete(res[0])
        await self.session.commit()

    async def save_models(self, *args):
        for arg in args:
            self.session.add(arg)
        await self.session.commit()
