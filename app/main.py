from fastapi import FastAPI
from app.api.v1.diary import router as diary_router

app = FastAPI(
    title="일기 CRUD API",
    description="FastAPI + SQLAlchemy 기반 일기 CRUD",
    version="1.0.0"
)

app.include_router(diary_router, prefix="/api/v1/diaries", tags=["diaries"])

@app.get("/")
def read_root():
    return {"message": "일기 CRUD API에 오신 것을 환영합니다!"}
