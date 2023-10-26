from fastapi import HTTPException

from models.users import Users
from repositories.users import UsersRepository


async def give_money(
        account_id: int,
        user: Users
):
    if user.id != account_id and not user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="You can only give money to yourself",
        )
    if user.id != account_id:
        user = await UsersRepository().find_one(id=account_id)

    data = {'balance': user.balance + 250000}
    await UsersRepository().edit_one(account_id, data)

