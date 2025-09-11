from fastapi import FastAPI

from app.routers import user

app = FastAPI(title="Diary Project")

app.include_router(user.router)
