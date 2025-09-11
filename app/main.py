from fastapi import FastAPI
from app.api.v1 import diary, quote, question, bookmark

app = FastAPI(
    title="일기 CRUD API",
    description="일기 CRUD + 명언 + 질문 + 북마크",
    version="1.0.0"
)

# 공통 prefix
app.include_router(diary.router, prefix="/api/v1")
app.include_router(quote.router, prefix="/api/v1")
app.include_router(question.router, prefix="/api/v1")
app.include_router(bookmark.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Diary 프로젝트에 오신 것을 환영합니다!"}