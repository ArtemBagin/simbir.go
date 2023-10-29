from fastapi import HTTPException
from sqlalchemy import select

from models.rents import Rents
from models.transports import Transports
from models.users import Users
from utils.repository import SQLAlchemyRepository


class RentsRepository(SQLAlchemyRepository):
    model = Rents

    @staticmethod
    async def check_rent(
            uow,
            user: Users,
            rent_id: int | None = None,
            transport_id: int | None = None,
            is_admin: bool = False
    ) -> tuple[list[Rents, Transports]]:
        """
        Возвращает join таблиц Rents и Transports по rent_id или transport_id
        :param uow: UnitOfWork
        :param user: Users
        :param rent_id: int
        :param transport_id: int
        :param is_admin: bool
        :return: tuple[list[Rents, Transports]]
        """
        if rent_id:
            stmt = select(Rents, Transports).join(Transports, Transports.id == Rents.transport_id).where(Rents.id == rent_id)
        else:
            stmt = select(Rents, Transports).join(Transports, Transports.id == Rents.transport_id).where(Transports.id == transport_id)

        res = await uow.session.execute(stmt)
        res = res.all()
        if not res:
            raise HTTPException(
                status_code=400,
                detail="Rentals with this id are not.",
            )
        rent, transport = res[0]
        if user.id not in (rent.user_id, transport.owner_id) and not is_admin:
            raise HTTPException(
                status_code=400,
                detail="This is not your rental.",
            )
        return res
