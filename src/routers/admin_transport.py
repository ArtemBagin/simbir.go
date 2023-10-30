from fastapi import APIRouter, Depends, status

from models.users import Users
from routers.dependencies import UOWDep
from schemas.transports import TransportAdmin, TransportAdminEdit, TransportRead
from security import get_current_admin
from services import transport_service

router = APIRouter(
    tags=["AdminTransportController"],
    prefix="/api/Admin/Transport",
    responses={404: {"description": "Not found"}}
)


@router.get('/', status_code=status.HTTP_200_OK, response_model=list[TransportRead])
async def get_transports_router(
        uow: UOWDep,
        _: Users = Depends(get_current_admin)
):
    res = await transport_service.get_transports(uow)
    return res


@router.get('/{pk}', status_code=status.HTTP_200_OK, response_model=TransportRead)
async def get_transport_by_id_router(
        uow: UOWDep,
        pk: int,
        _: Users = Depends(get_current_admin)
):
    res = await transport_service.get_transport_by_id(uow, pk)
    return res


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=TransportRead)
async def create_transport_router(
        uow: UOWDep,
        data: TransportAdmin,
        _: Users = Depends(get_current_admin)
):
    res = await transport_service.create_transport(uow, data)
    return res


@router.put('/{pk}', status_code=status.HTTP_204_NO_CONTENT)
async def edit_one_transport_router(
        uow: UOWDep,
        pk: int,
        data: TransportAdminEdit,
        user: Users = Depends(get_current_admin)
):
    await transport_service.edit_one_transport(uow, user, data, pk, is_admin=True)


@router.delete('/{pk}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_one_transport_router(
        uow: UOWDep,
        pk: int,
        user: Users = Depends(get_current_admin)
):
    await transport_service.delete_one_transport(uow, user, pk, is_admin=True)
