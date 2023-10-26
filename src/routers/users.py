from fastapi import APIRouter, Depends, status

from models.users import Users
from schemas.users import UserCreate, UserRead
from security import get_current_user
from services import user_service

router = APIRouter(
    tags=["AccountController"],
    prefix="/api/Account",
    responses={404: {"description": "Not found"}}
)


@router.post('/SignUp', status_code=status.HTTP_201_CREATED)
async def create_user_router(data: UserCreate):
    res = await user_service.create_user(data)
    return res


@router.get('/Me', status_code=status.HTTP_200_OK, response_model=UserRead)
def get_user_detail_router(user: Users = Depends(get_current_user)):
    return user


@router.put('/Update', status_code=status.HTTP_204_NO_CONTENT)
async def edit_user_router(
        data: UserCreate,
        user: Users = Depends(get_current_user)
):
    await user_service.update_user(user, data)

