from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.base import Base
from app.db.session import engine
from app.api.v1 import quote, question, bookmark

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 애플리케이션 시작 시 실행되는 코드
    print("애플리케이션 시작...")
    await init_db()
    yield
    # 애플리케이션 종료 시 실행되는 코드
    print("애플리케이션 종료...")
app = FastAPI(lifespan=lifespan)

app.include_router(quote.router)
app.include_router(question.router)
app.include_router(bookmark.router)
from fastapi import FastAPI
from app.api.v1.diary import router as diary_router

app = FastAPI(
    title="일기 CRUD API",
    description="FastAPI + SQLAlchemy 기반 일기 CRUD",
    version="1.0.0"
)

app.include_router(diary_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "일기 CRUD API에 오신 것을 환영합니다!"}



@app.get("/")
def read_root():
    return {"명언 및 북마크 API에 오신 것을 환영합니다!"}