from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import Boolean, Double, Integer

from database.database import Base


class Transports(Base):
    owner_id: Mapped[str] = mapped_column(Integer, ForeignKey('users.id', ondelete='CASCADE'),
                                          nullable=False, name='ownerId')
    can_be_rented: Mapped[bool] = mapped_column(Boolean, nullable=False, name='canBeRented')
    transport_type: Mapped[str] = mapped_column(String, nullable=False, name='transportType')
    model: Mapped[str] = mapped_column(String, nullable=False)
    color: Mapped[str] = mapped_column(String, nullable=False)
    identifier: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    latitude: Mapped[float] = mapped_column(Double, nullable=False)
    longitude: Mapped[float] = mapped_column(Double, nullable=False)
    minute_price: Mapped[float] = mapped_column(Double, name='minutePrice')
    day_price: Mapped[float] = mapped_column(Double, name='dayPrice')
