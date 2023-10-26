from fastapi import HTTPException
from fastapi.responses import JSONResponse

from repositories.users import UsersRepository
from schemas.users import UserAdmin, UserCreate
from security import get_password_hash


async def create_user(data: UserCreate | UserAdmin):
    user = await UsersRepository().find_one(username=data.username)

    if user:
        raise HTTPException(
            status_code=422,
            detail="Email is already registered with us."
        )

    data = data.model_dump()
    data['password'] = get_password_hash(data['password'])
    await UsersRepository().add_one(data)
    payload = {"message": "User account has been succesfully created."}

    return JSONResponse(content=payload)


async def update_user(user, data: UserAdmin | UserCreate):
    if user.username != data.username:
        raise HTTPException(
            status_code=422,
            detail="A user with the same name already exists."
        )

    data.password = get_password_hash(data.password)
    await UsersRepository().find_one(username=data.username)
    res = await UsersRepository().edit_one(id=user.id, data=data.model_dump(exclude_none=True))
    return res


async def get_users():
    users = await UsersRepository().find_all()
    return users


async def get_user_by_id(
        pk: int
):
    user = await UsersRepository().find_one(id=pk)
    return user


async def update_user_by_id(
        user_id: int,
        data: UserAdmin,
):
    user = await UsersRepository().find_one(id=user_id)
    if not data.username:
        data.username = user.username
    if not data.password:
        data.password = user.password
    res = await update_user(user, data)
    return res


async def del_user(
        pk: int,
):
    await UsersRepository().delete_one(id=pk)


