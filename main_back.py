# -*- coding: UTF-8 -*-

from fastapi import Depends, FastAPI, HTTPException, status
import uvicorn
from dependencies import get_query_token, get_token_header
from internal import admin
from routers import items, users
from pydantic import BaseModel
import pandas as pd
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}
app = FastAPI(
    dependencies=[Depends(get_query_token)]
)

app.include_router(users.router)
app.include_router(items.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)


class User(BaseModel):
    userName: str
    passward: str


class UserInDB(User):
    hashed_password: str


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}


def fake_hash_password(password: str):
    return "fakehashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    return user


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


# @app.post("/login")
# def login(user: User):
#     author = pd.read_excel("static_db/authoraztion.xlsx")
#     print(user)
#     print(author['userName'].tolist())
#     if user.userName in author['userName'].tolist():
#         if author.loc[author['userName'] == user.userName, "password"][0] == user.passward:
#             return True
#     return False


# @app.get("/items/")
# async def read_items(token: str = Depends(oauth2_scheme)):
#     return {"token": token}


if __name__ == '__main__':
    uvicorn.run(app, host="192.168.146.239", port=8000)
