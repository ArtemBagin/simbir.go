from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import Boolean, Double, Integer

from database.database import Base
from schemas.transports import TransportSchema


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

    def to_read_model(self) -> TransportSchema:
        return TransportSchema(
            id=self.id,
            owner_id=self.owner_id,
            can_be_rented=self.can_be_rented,
            transport_type=self.transport_type,
            model=self.model,
            color=self.color,
            identifier=self.identifier,
            description=self.description,
            latitude=self.latitude,
            longitude=self.longitude,
            minute_price=self.minute_price,
            day_price=self.day_price
        )
