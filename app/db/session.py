# app/db/session.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# MySQL Async URL (aiomysql 사용)
DATABASE_URL = "mysql+aiomysql://diary_user:qwer1234@localhost:3306/diary_db"

# AsyncEngine 생성
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # 쿼리 로그 확인
)

# AsyncSession 생성
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# FastAPI 의존성 함수
async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session
