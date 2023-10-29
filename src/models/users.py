from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import Boolean, Double

from database.database import Base
from schemas.users import UserSchema


class Users(Base):
    username: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, name='isAdmin')
    balance: Mapped[float] = mapped_column(Double, nullable=False, default=0)

    def to_read_model(self) -> UserSchema:
        return UserSchema(
            id=self.id,
            username=self.username,
            password=self.password,
            is_admin=self.is_admin,
            balance=self.balance
        )

