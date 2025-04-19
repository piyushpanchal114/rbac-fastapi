from fastapi import FastAPI
from controllers import users_api, auth_api

app = FastAPI()

app.include_router(auth_api.router)
app.include_router(users_api.router)


@app.get("/ping")
async def ping():
    return {"ping": "pong"}
