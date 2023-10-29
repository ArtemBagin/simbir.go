from fastapi import APIRouter, Depends, status

from models.users import Users
from routers.dependencies import UOWDep
from security import get_current_user
from services import paymant_service

router = APIRouter(
    prefix="/api/Payment",
    tags=["PaymentController"],
    responses={404: {"description": "Not found"}},
)


@router.post('/Hesoyam/{account_id}', status_code=status.HTTP_200_OK)
async def give_money_router(
        uow: UOWDep,
        account_id: int,
        user: Users = Depends(get_current_user)
):
    await paymant_service.give_money(account_id, user, uow)
    return {'status': 'success'}

