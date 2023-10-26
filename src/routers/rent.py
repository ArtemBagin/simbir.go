from fastapi import APIRouter, Depends, status

from models.users import Users
from schemas.rents import EndRend, RentReed, RentType
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
        lat: float,
        long: float,
        radius: float,
        type: str,
):
    res = await rent_service.accessible_transport(lat, long, radius, type)
    return res


@router.get('/MyHistory', status_code=status.HTTP_200_OK, response_model=list[RentReed])
async def get_history_router(
        user: Users = Depends(get_current_user)
):
    res = await rent_service.get_history_by_user_id(user)
    return res


@router.get('/TransportHistory/{transport_id}', status_code=status.HTTP_200_OK, response_model=list[RentReed])
async def get_transport_history_router(
        transport_id: int,
        user: Users = Depends(get_current_user)
):
    res = await rent_service.get_transport_history_by_id(transport_id, user)
    return res


@router.get('/{rent_id}', status_code=status.HTTP_200_OK, response_model=RentReed)
async def check_my_rent_router(
        rent_id: int,
        user: Users = Depends(get_current_user)
):
    res = await rent_service.check_my_rent(rent_id, user)
    return res


@router.post('/New/{transport_id}', status_code=status.HTTP_201_CREATED)
async def new_rent_router(
        transport_id: int,
        rent_type: RentType,
        user: Users = Depends(get_current_user),
):
    res = await rent_service.new_rent(transport_id, rent_type, user)
    return res


@router.post('/End/{rent_id}', status_code=status.HTTP_200_OK, response_model=RentReed)
async def end_my_rent_router(
        rent_id: int,
        geo: EndRend,
        user: Users = Depends(get_current_user)
):
    res = await rent_service.end_my_rent(rent_id, geo, user)
    return res

