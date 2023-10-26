from datetime import datetime

from fastapi import HTTPException

from models.rents import Rents
from models.users import Users
from repositories.rents import RentsRepository
from repositories.transports import TransportsRepository
from repositories.users import UsersRepository
from schemas.rents import EndRend, RentBase, RentEdit, RentType, RentTypes
from schemas.transports import TransportTypes


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


async def accessible_transport(lat: float, long: float, radius: float, type: str):
    if type != TransportTypes.all:
        res = await TransportsRepository().find(transport_type=type)
    else:
        res = await TransportsRepository().find()
    res = filter(lambda x: in_circle(lat, long, radius, x.latitude, x.longitude), res)
    return list(res)


async def check_my_rent(
        rent_id: int,
        user: Users
):
    res = await RentsRepository.check_rent(user, rent_id=rent_id)
    return res[0][0]


async def get_history_by_user_id(
        user: Users,
        pk: int | None = None
):
    if user.is_admin and pk:
        rents = await RentsRepository().find(user_id=pk)
    else:
        rents = await RentsRepository().find(user_id=user.id)
    return rents


async def get_transport_history_by_id(
        transport_id: int,
        user: Users,
):
    res = await RentsRepository.check_rent(user, transport_id=transport_id)
    res = [i[0] for i in res]
    return res


async def new_rent(
        transport_id: int,
        rent_type: RentType,
        user: Users
):
    transport = await TransportsRepository().find_one(id=transport_id)
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

    rent = Rents(
        transport_id=transport.id,
        user_id=user.id,
        price_of_unit=price_of_unit,
        price_type=rent_type.price_type
    )
    await TransportsRepository.save_models(transport, rent)
    return rent


async def end_my_rent(
        rent_id: int,
        geo: EndRend,
        user: Users
):
    user = await UsersRepository().find_one(id=user.id)
    res = await RentsRepository.check_rent(user, rent_id=rent_id)
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
    await UsersRepository.save_models(user, rent, transport)
    return rent


async def create_rent(
        rent: RentBase,
):
    res = await RentsRepository().add_one(rent.model_dump())
    return res


async def end_rent_by_user_id(
        rent_id: int,
        end_rent: EndRend,
):
    user = await UsersRepository().find_one(id=end_rent.user_id)
    res = await end_my_rent(rent_id, end_rent, user)
    return res


async def edit_rent(
        pk: int,
        data: RentEdit,
):
    await RentsRepository().find_one(id=pk)
    res = await RentsRepository().edit_one(pk, data.model_dump(exclude_none=True))
    return res


async def delete_rent(
        pk: int
):
    await RentsRepository().delete_one(id=pk)
