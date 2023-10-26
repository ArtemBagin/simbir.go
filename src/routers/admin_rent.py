from fastapi import APIRouter, Depends, status

from models.users import Users
from schemas.rents import EndRendAdmin, RentBase, RentEdit, RentReed
from security import get_current_admin
from services import rent_service

router = APIRouter(
    tags=["AdminRentController"],
    prefix="/api/Admin/Rent",
    responses={404: {"description": "Not found"}}
)


@router.get('/{rent_id}', status_code=status.HTTP_200_OK, response_model=RentReed)
async def check_my_rent_router(
        rent_id: int,
        user: Users = Depends(get_current_admin)
):
    res = await rent_service.check_my_rent(rent_id, user)
    return res


@router.get('/UserHistory/{pk}', status_code=status.HTTP_200_OK, response_model=list[RentReed])
async def get_history_router(
        pk: int,
        user: Users = Depends(get_current_admin)
):
    res = await rent_service.get_history_by_user_id(user, pk)
    return res


@router.get('/TransportHistory/{transport_id}', status_code=status.HTTP_200_OK, response_model=list[RentReed])
async def get_transport_history_router(
        transport_id: int,
        user: Users = Depends(get_current_admin)
):
    res = await rent_service.get_transport_history_by_id(transport_id, user)
    return res


@router.post('/', status_code=status.HTTP_200_OK)
async def create_rent_router(
        rent: RentBase,
        _: Users = Depends(get_current_admin)
):
    res = await rent_service.create_rent(rent)
    return res


@router.post('/End/{rent_id}', status_code=status.HTTP_200_OK, response_model=RentReed)
async def end_my_rent_router(
        rent_id: int,
        end_rent: EndRendAdmin,
        _: Users = Depends(get_current_admin)
):
    res = await rent_service.end_rent_by_user_id(rent_id, end_rent)
    return res


@router.put('/{pk}', status_code=status.HTTP_204_NO_CONTENT)
async def edit_rent_router(
        pk: int,
        data: RentEdit,
        _: Users = Depends(get_current_admin)
):
    await rent_service.edit_rent(pk, data)


@router.delete('/{pk}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_rent_router(
        pk: int,
        _: Users = Depends(get_current_admin)
):
    await rent_service.delete_rent(pk)

