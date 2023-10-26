from pydantic import BaseModel


class SegmentBase(BaseModel):
    start: int
    count: int


class TransportSegment(SegmentBase):
    transport_type: str

