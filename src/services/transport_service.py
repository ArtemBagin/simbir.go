from fastapi import HTTPException

from models.users import Users
from schemas.transports import TransportBase, TransportEdit
from utils.unitofwork import UnitOfWork


async def get_transport_by_id(
        uow: UnitOfWork,
        pk: int
):
    async with uow:
        transport = await uow.transports.find_one(id=pk)
        return transport


async def create_transport(
        uow: UnitOfWork,
        data: TransportBase,
        owner_id: int = None
):
    async with uow:
        if not owner_id:
            res = await uow.transports.add_one(data.model_dump())
        else:
            data = data.model_dump()
            data['owner_id'] = owner_id
            res = await uow.transports.add_one(data)
        return res


async def edit_one_transport(
        uow: UnitOfWork,
        user: Users,
        data: TransportEdit,
        pk,
        is_admin=False
):
    async with uow:
        transport = await uow.transports.find_one(id=pk)

        if user.id != transport.owner_id and not is_admin:
            raise HTTPException(
                status_code=400,
                detail="Invalid request, no such data exists.",
            )

        res = await uow.transports.edit_one(pk, data.model_dump(exclude_none=True))
        return res


async def delete_one_transport(
        uow: UnitOfWork,
        user: Users,
        pk: int,
        is_admin=False
):
    async with uow:
        transport = await uow.transports.find_one(id=pk)
        if user.id != transport.owner_id and not is_admin:
            await uow.transports.delete_one(id=pk)


async def get_transports(uow: UnitOfWork):
    async with uow:
        res = await uow.transports.find_all()
        return res

