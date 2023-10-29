from fastapi import APIRouter, Depends, status

from models.users import Users
from routers.dependencies import UOWDep
from schemas.transports import TransportBase, TransportEdit, TransportRead
from security import get_current_user
from services import transport_service

router = APIRouter(
    tags=['TransportController'],
    prefix='/api/Transport',
    responses={404: {"description": "Not found"}}
)


@router.get('/{pk}', status_code=status.HTTP_200_OK, response_model=TransportRead)
async def get_transport_router(
        uow: UOWDep,
        pk: int
):
    res = await transport_service.get_transport_by_id(uow, pk)
    return res


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=TransportRead)
async def create_transport_router(
        uow: UOWDep,
        data: TransportBase,
        user: Users = Depends(get_current_user),
):
    res = await transport_service.create_transport(uow, data, owner_id=user.id)
    return res


@router.put('/{pk}', status_code=status.HTTP_204_NO_CONTENT)
async def edit_one_transport_router(
        uow: UOWDep,
        pk: int,
        data: TransportEdit,
        user: Users = Depends(get_current_user),
):
    await transport_service.edit_one_transport(uow, user, data, pk)


@router.delete('/{pk}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_transport_router(
        uow: UOWDep,
        pk: int,
        user: Users = Depends(get_current_user),
):
    await transport_service.delete_one_transport(uow, user, pk)

