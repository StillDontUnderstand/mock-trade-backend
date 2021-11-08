from fastapi import Depends, FastAPI, HTTPException, status
import uvicorn
import authoraztion as auth
from routers import users



app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)

if __name__ == '__main__':
    # uvicorn.run(app, host="192.168.146.239", port=8000)
    uvicorn.run(app, host="127.0.0.1", port=8000)
