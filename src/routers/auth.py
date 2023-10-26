from fastapi import APIRouter, Depends, Header, status
from fastapi.security import OAuth2PasswordRequestForm

from blacklist.service import blacklist
from models.users import Users
from security import get_current_user, oauth2_scheme
from services import auth_service

router = APIRouter(
    prefix="/api/Account",
    tags=["AccountController"],
    responses={404: {"description": "Not found"}}
)


@router.post("/SignIn", status_code=status.HTTP_200_OK)
async def authenticate_user(data: OAuth2PasswordRequestForm = Depends()):
    res = await auth_service.get_token(data)
    return res


@router.post("/SignOut", status_code=status.HTTP_200_OK)
async def sing_out_user(
        token: str = Depends(oauth2_scheme),
        _: Users = Depends(get_current_user)
):
    blacklist.add_blacklist_token(token)


@router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh_access_token(refresh_token: str = Header()):
    res = await auth_service.get_refresh_token(token=refresh_token)
    return res

