from fastapi import APIRouter
from pydantic import BaseModel
import pandas as pd

router = APIRouter(
    prefix="/users",
)


class User(BaseModel):
    userName: str
    passward: str


@router.get("/", tags=["users"])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/me", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}


@router.post("/verify", tags=["users"])
def login(user: User):
    author = pd.read_excel("static_db/authoraztion.xlsx")
    print(user)
    print(author['userName'].tolist())
    if user.userName in author['userName'].tolist():
        if author.loc[author['userName'] == user.userName, "password"][0] == user.passward:
            return True
    return False
