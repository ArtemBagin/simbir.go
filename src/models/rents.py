from datetime import datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import TIMESTAMP, Double, Integer

from database.database import Base
from schemas.rents import RentTypes, RentSchema


class Rents(Base):
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id', ondelete='CASCADE'),
                                         nullable=False, name='userId')
    transport_id: Mapped[int] = mapped_column(Integer, ForeignKey('transports.id', ondelete='CASCADE'),
                                              nullable=False, name='transportId')
    time_start: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow, name='timeStart')
    time_end: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=True, name='timeEnd')
    price_of_unit: Mapped[float] = mapped_column(Double, nullable=False, name='priceOfUnit')
    price_type: Mapped[str] = mapped_column(String, nullable=False, name='priceType')
    final_price: Mapped[int] = mapped_column(Integer, nullable=True, default=0, name='finalPrice')

    def calc_final_price(self):
        delta = datetime.utcnow() - self.time_start
        if self.price_type == RentTypes.minutes:
            return self.price_of_unit * (delta.seconds // 60 + 60)
        else:
            return self.price_of_unit * (delta.days+1)

    def to_read_model(self) -> RentSchema:
        return RentSchema(
            id=self.id,
            user_id=self.user_id,
            transport_id=self.transport_id,
            time_start=self.time_start,
            time_end=self.time_end,
            price_of_unit=self.price_of_unit,
            price_type=self.price_type,
            final_price=self.final_price
        )
