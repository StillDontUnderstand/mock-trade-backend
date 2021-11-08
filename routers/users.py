from fastapi import APIRouter
from pydantic import BaseModel
from fastapi import Depends
from authoraztion import get_current_active_user

router = APIRouter(
    prefix="/users",
)


class User(BaseModel):
    userName: str
    passward: str


@router.get("/info")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]


