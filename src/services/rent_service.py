from datetime import datetime

from fastapi import HTTPException

from models.users import Users
from repositories.rents import RentsRepository
from schemas.rents import EndRend, RentBase, RentEdit, RentType, RentTypes
from schemas.transports import TransportTypes
from utils.unitofwork import UnitOfWork


def in_circle(x0, y0, r, x1, y1) -> bool:
    """
    Функция для проверки, входит ли точка в заданный радиус
    :param x0: latitude местоположение
    :param y0: longitude местоположения
    :param r: радиус
    :param x1: latitude транспорта
    :param y1: longitude транспорта
    :return: bool
    """
    res = (x1 - x0) ** 2 + (y1 - y0) ** 2 <= r ** 2
    return res


async def accessible_transport(
        uow: UnitOfWork,
        lat: float,
        long: float,
        radius: float,
        transport_type: str
):
    async with uow:
        if transport_type != TransportTypes.all:
            res = await uow.transports.find(transport_type=transport_type)
        else:
            res = await uow.transports.find()
        res = list(filter(lambda x: in_circle(lat, long, radius, x.latitude, x.longitude), res))
        return res


async def check_my_rent(
        uow: UnitOfWork,
        rent_id: int,
        user: Users
):
    async with uow:
        res = await RentsRepository.check_rent(uow, user, rent_id=rent_id)
        return res[0][0].to_read_model()


async def get_history_by_user_id(
        uow: UnitOfWork,
        user: Users,
        pk: int | None = None,
        is_admin: bool = False
):
    async with uow:
        if is_admin and pk:
            rents = await uow.rents.find(user_id=pk)
        else:
            rents = await uow.rents.find(user_id=user.id)
        print(rents)
        return rents


async def get_transport_history_by_id(
        uow: UnitOfWork,
        transport_id: int,
        user: Users,
        is_admin: bool = False
):
    async with uow:
        res = await RentsRepository.check_rent(uow, user, transport_id=transport_id, is_admin=is_admin)
        res = [i[0].to_read_model() for i in res]
        return res


async def new_rent(
        uow: UnitOfWork,
        transport_id: int,
        rent_type: RentType,
        user: Users
):
    async with uow:
        transport = await uow.transports.find_one(raw=True, id=transport_id)
        if transport.owner_id == user.id:
            raise HTTPException(
                status_code=400,
                detail="You cannot rent your own transport.",
            )
        if not transport.can_be_rented:
            raise HTTPException(
                status_code=400,
                detail="This transport is busy.",
            )
        if user.balance <= 0:
            raise HTTPException(
                status_code=400,
                detail="You don't have money.",
            )

        transport.can_be_rented = False
        if rent_type.price_type == RentTypes.minutes:
            price_of_unit = transport.minute_price
        else:
            price_of_unit = transport.day_price

        rent = await uow.rents.add_one({
            'transport_id': transport.id,
            'user_id': user.id,
            'price_of_unit': price_of_unit,
            'price_type': rent_type.price_type
        })

        return rent.to_read_model()


async def end_rent_by_id(
        uow: UnitOfWork,
        rent_id: int,
        geo: EndRend,
        user: Users
):
    user = await uow.users.find_one(raw=True, id=user.id)
    res = await RentsRepository.check_rent(uow, user, rent_id=rent_id)
    rent, transport = res[0]

    if (user.id != rent.user_id) or rent.final_price:
        raise HTTPException(
            status_code=400,
            detail="This is not user rental.",
        )

    final_price = rent.calc_final_price()
    user.balance -= final_price
    rent.final_price = final_price
    rent.time_end = datetime.utcnow()
    transport.can_be_rented = True
    transport.latitude = geo.lat
    transport.longitude = geo.long
    await uow.session.commit()
    return rent


async def end_my_rent(
        uow: UnitOfWork,
        rent_id: int,
        geo: EndRend,
        user: Users
):
    async with uow:
        res = await end_rent_by_id(uow, rent_id, geo, user)
        return res


async def create_rent(
        uow: UnitOfWork,
        rent: RentBase,
):
    async with uow:
        res = await uow.rents.add_one(rent.model_dump())
        return res


async def end_rent_by_user_id(
        uow: UnitOfWork,
        rent_id: int,
        end_rent: EndRend,
):
    async with uow:
        user = await uow.users.find_one(id=end_rent.user_id)
        res = await end_rent_by_id(uow, rent_id, end_rent, user)
        return res


async def edit_rent(
        uow: UnitOfWork,
        pk: int,
        data: RentEdit,
):
    async with uow:
        await uow.rents.find_one(id=pk)
        res = await uow.rents.edit_one(pk, data.model_dump(exclude_none=True))
        return res


async def delete_rent(
        uow: UnitOfWork,
        pk: int
):
    async with uow:
        await uow.rents.delete_one(id=pk)
