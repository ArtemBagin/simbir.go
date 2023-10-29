from fastapi import APIRouter, Depends, status

from models.users import Users
from routers.dependencies import UOWDep
from schemas.users import UserAdmin, UserRead
from security import get_current_admin
from services import user_service

router = APIRouter(
    tags=["AdminAccountController"],
    prefix="/api/Admin/Account",
    responses={404: {"description": "Not found"}}
)


@router.get('/', status_code=status.HTTP_200_OK, response_model=list[UserRead])
async def get_users_router(
        uow: UOWDep,
        _: Users = Depends(get_current_admin),
):
    res = await user_service.get_users(uow)
    return res


@router.get('/{pk}', status_code=status.HTTP_200_OK, response_model=UserRead)
async def get_user_by_id_router(
        uow: UOWDep,
        pk: int,
        _: Users = Depends(get_current_admin)
):
    res = await user_service.get_user_by_id(uow, pk)
    return res


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user_router(
        uow: UOWDep,
        data: UserAdmin,
        _: Users = Depends(get_current_admin)
):
    res = await user_service.create_user(uow, data)
    return res


@router.put('/{pk}', status_code=status.HTTP_204_NO_CONTENT)
async def update_user_router(
        uow: UOWDep,
        pk: int,
        data: UserAdmin,
        _: Users = Depends(get_current_admin)
):
    await user_service.update_user_by_id(uow, pk, data)


@router.delete('/{pk}', status_code=status.HTTP_204_NO_CONTENT)
async def del_user_router(
        uow: UOWDep,
        pk: int,
        _: Users = Depends(get_current_admin)
):
    await user_service.del_user(uow, pk)
