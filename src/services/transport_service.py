from fastapi import HTTPException

from models.users import Users
from repositories.transports import TransportsRepository
from schemas.transports import TransportBase, TransportEdit


async def permission_check_transport(user: Users, pk: int):
    transport = await TransportsRepository().find_one(id=pk)
    if user.id != transport.owner_id and not user.is_admin:
        raise HTTPException(
            status_code=400,
            detail="Invalid request, no such data exists.",
        )
    return transport


async def get_transport_by_id(pk: int):
    transport = await TransportsRepository().find_one(id=pk)
    return transport


async def create_transport(data: TransportBase, owner_id: int = None):
    if not owner_id:
        res = await TransportsRepository().add_one(data.model_dump())
    else:
        data = data.model_dump()
        data['owner_id'] = owner_id
        res = await TransportsRepository().add_one(data)
    return res


async def edit_one_transport(user: Users, data: TransportEdit, pk):
    await permission_check_transport(user, pk)
    res = await TransportsRepository().edit_one(pk, data.model_dump(exclude_none=True))
    return res


async def delete_one_transport(user: Users, pk: int):
    await TransportsRepository().delete_one(id=pk)


async def get_transports():
    res = await TransportsRepository().find_all()
    return res

