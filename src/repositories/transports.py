from models.transports import Transports
from utils.repository import SQLAlchemyRepository


class TransportsRepository(SQLAlchemyRepository):
    model = Transports
