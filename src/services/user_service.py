from fastapi import HTTPException
from fastapi.responses import JSONResponse

from schemas.users import UserAdmin, UserCreate
from security import get_password_hash
from utils.unitofwork import UnitOfWork


async def create_user(uow: UnitOfWork, data: UserCreate | UserAdmin):
    async with uow:
        user = await uow.users.find_one(username=data.username, raw=True, no_error=True)

        if user:
            raise HTTPException(
                status_code=422,
                detail="Username is already registered with us."
            )

        data = data.model_dump()
        data['password'] = get_password_hash(data['password'])
        await uow.users.add_one(data)
        payload = {"message": "User account has been succesfully created."}

        return JSONResponse(content=payload)


async def update_user(uow: UnitOfWork, user, data: UserAdmin | UserCreate):
    data.password = get_password_hash(data.password)
    async with uow:
        named_user = await uow.users.find_one(username=data.username, no_error=True)
        if named_user and named_user.username != user.username:
            raise HTTPException(
                status_code=422,
                detail="A user with the same name already exists."
            )
        res = await uow.users.edit_one(id=user.id, data=data.model_dump(exclude_none=True))
        return res


async def get_users(uow: UnitOfWork):
    async with uow:
        users = await uow.users.find_all()
        return users


async def get_user_by_id(
        uow: UnitOfWork,
        pk: int
):
    async with uow:
        user = await uow.users.find_one(id=pk)
        return user


async def update_user_by_id(
        uow: UnitOfWork,
        user_id: int,
        data: UserAdmin
):
    async with uow:
        user = await uow.users.find_one(id=user_id)
        if not data.username:
            data.username = user.username
        if not data.password:
            data.password = user.password
        res = await update_user(user, data)
        return res


async def del_user(
        uow: UnitOfWork,
        pk: int
):
    await uow.users.delete_one(id=pk)


