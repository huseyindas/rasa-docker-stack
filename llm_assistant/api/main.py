from fastapi import FastAPI

from .routes import assistants_router


app = FastAPI()

app.include_router(assistants_router)

@app.get("/")
async def ping():
    return {"ping": "pong"}
