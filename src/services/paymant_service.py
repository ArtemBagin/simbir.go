from fastapi import HTTPException

from models.users import Users
from utils.unitofwork import UnitOfWork


async def give_money(
        uow: UnitOfWork,
        account_id: int,
        user: Users
):
    if user.id != account_id and not user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="You can only give money to yourself",
        )

    async with uow:
        user = await uow.users.find_one(raw=True, id=account_id)
        user.balance += 250000
        await uow.session.commit()

