from dataclasses import dataclass

from pydantic import BaseModel, field_validator


@dataclass
class TransportTypes:
    car = 'car'
    bike = 'bike'
    scooter = 'scooter'
    all = 'all'


class TransportType(BaseModel):
    transport_type: str

    @field_validator('transport_type')
    @classmethod
    def validate_rent_type(cls, rent_type: str) -> str:
        if rent_type not in [TransportTypes.car, TransportTypes.bike, TransportTypes.scooter]:
            raise ValueError('TransportType must been car, bike or scooter')
        return rent_type


class TransportBase(TransportType):
    can_be_rented: bool
    model: str
    color: str
    identifier: str
    description: str | None
    latitude: float
    longitude: float
    minute_price: float | None
    day_price: float | None


class TransportSchema(TransportBase):
    id: int
    owner_id: int


class TransportEdit(BaseModel):
    can_be_rented: bool | None = None
    transport_type: str | None = None
    model: str | None = None
    color: str | None = None
    identifier: str | None = None
    description: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    minute_price: float | None = None
    day_price: float | None = None

    @field_validator('transport_type')
    @classmethod
    def validate_rent_type(cls, rent_type: str) -> str | None:
        if rent_type not in [TransportTypes.car, TransportTypes.bike, TransportTypes.scooter]:
            return None
        return rent_type


class TransportAdminEdit(TransportEdit):
    owner_id: int | None = None


class TransportRead(TransportBase):
    id: int
    owner_id: int


class TransportAdmin(TransportBase):
    owner_id: int
