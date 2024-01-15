from fastapi import FastAPI
import uvicorn

from Routers.mainRouter import router


app = FastAPI()

app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port="8000")