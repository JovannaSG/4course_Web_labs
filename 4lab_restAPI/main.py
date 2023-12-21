from fastapi import FastAPI

from Routers.mainRouter import router
from Routers.authRouter import auth_router


app = FastAPI()

app.include_router(router)
app.include_router(auth_router)
