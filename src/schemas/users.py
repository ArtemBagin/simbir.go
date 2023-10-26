from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserRead(UserBase):
    id: int
    balance: int
    is_admin: bool


class UserCreate(UserBase):
    password: str


class UserAdmin(UserBase):
    username: str | None = None
    balance: int | None = None
    is_admin: bool | None = None
    password: str | None = None


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'Bearer'
    expires_in: int

