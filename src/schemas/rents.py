from dataclasses import dataclass
from datetime import datetime

from pydantic import BaseModel, field_validator


@dataclass
class RentTypes:
    days = 'days'
    minutes = 'minutes'


class RentType(BaseModel):
    price_type: str

    @field_validator('price_type')
    @classmethod
    def validate_rent_type(cls, rent_type: str) -> str:
        if rent_type not in [RentTypes.days, RentTypes.minutes]:
            raise ValueError('RentType must been Minutes or Days')
        return rent_type


class RentBase(RentType):
    transport_id: int
    user_id: int
    price_of_unit: float
    price_type: str


class RentEdit(BaseModel):
    transport_id: int | None = None
    user_id: int | None = None
    time_start: datetime | None = None
    time_end: datetime | None = None
    price_of_unit: float | None = None
    price_type: str | None = None
    final_price: int | None = None


class RentReed(RentBase):
    id: int
    time_start: datetime = None
    time_end: datetime | None = None
    final_price: float | None = None


class EndRend(BaseModel):
    lat: float
    long: float


class EndRendAdmin(EndRend):
    user_id: int
