from models.transports import Transports
from repositories.repository import SQLAlchemyRepository


class TransportsRepository(SQLAlchemyRepository):
    model = Transports
