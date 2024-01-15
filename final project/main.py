from fastapi import FastAPI
import uvicorn

from Routers.clientRouter import client_router
from Routers.managerRouter import manager_router


app = FastAPI()

app.include_router(manager_router)
app.include_router(client_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port="8000")