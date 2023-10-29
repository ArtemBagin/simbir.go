from fastapi import APIRouter, Depends, status

from models.users import Users
from routers.dependencies import UOWDep
from schemas.rents import EndRend, RentReed, RentType, RentSchema
from schemas.transports import TransportRead
from security import get_current_user
from services import rent_service

router = APIRouter(
    tags=['RentController'],
    prefix='/api/Rent',
    responses={404: {"description": "Not found"}}
)


@router.get('/Transport', status_code=status.HTTP_200_OK, response_model=list[TransportRead])
async def accessible_transport_router(
        uow: UOWDep,
        lat: float,
        long: float,
        radius: float,
        transport_type: str,
):
    res = await rent_service.accessible_transport(uow, lat, long, radius, transport_type)
    return res


@router.get('/MyHistory', status_code=status.HTTP_200_OK, response_model=list[RentReed])
async def get_history_router(
        uow: UOWDep,
        user: Users = Depends(get_current_user)
):
    res = await rent_service.get_history_by_user_id(uow, user)
    return res


@router.get('/TransportHistory/{transport_id}', status_code=status.HTTP_200_OK, response_model=list[RentReed])
async def get_transport_history_router(
        uow: UOWDep,
        transport_id: int,
        user: Users = Depends(get_current_user)
):
    res = await rent_service.get_transport_history_by_id(uow, transport_id, user)
    return res


@router.get('/{rent_id}', status_code=status.HTTP_200_OK, response_model=RentReed)
async def check_my_rent_router(
        uow: UOWDep,
        rent_id: int,
        user: Users = Depends(get_current_user)
):
    res = await rent_service.check_my_rent(uow, rent_id, user)
    return res


@router.post('/New/{transport_id}', status_code=status.HTTP_201_CREATED, response_model=RentSchema)
async def new_rent_router(
        uow: UOWDep,
        transport_id: int,
        rent_type: RentType,
        user: Users = Depends(get_current_user),
):
    res = await rent_service.new_rent(uow, transport_id, rent_type, user)
    return res


@router.post('/End/{rent_id}', status_code=status.HTTP_200_OK, response_model=RentReed)
async def end_my_rent_router(
        uow: UOWDep,
        rent_id: int,
        geo: EndRend,
        user: Users = Depends(get_current_user)
):
    res = await rent_service.end_my_rent(uow, rent_id, geo, user)
    return res

