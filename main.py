# -*- coding: UTF-8 -*-

from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from typing import Optional
import pandas as pd


app = FastAPI()


class User(BaseModel):
    userName: str
    passward: str


@app.get("/")
async def main():
    return {"message": "Hello，FastAPI"}


@app.post("/login")
def login(user: User):
    author = pd.read_excel("static_db/authoraztion.xlsx")
    print(user)
    print(author['userName'].tolist())
    if user.userName in author['userName'].tolist():
        if author.loc[author['userName'] == user.userName, "password"][0] == user.passward:
            return True
    return False


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
