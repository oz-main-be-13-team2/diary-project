import os
from typing import AsyncGenerator
from dotenv import load_dotenv # .env 파일 로드를 위한 라이브러리
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


# 비동기 엔진 생성
engine = create_async_engine(
    DATABASE_URL,
    echo=True # 개발 중 쿼리 로그 확인용으로 True로 설정
)

# 비동기 세션 생성기 / DB와 상호작용
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False # 커밋이 완료된 후에도 세션에 있는 객체들을 만료시키지 않도록 설정
    # False로 설정하면, 커밋 후에도 객체에 접근할 수 있어 객체 상태 유지에 유리
)

# Fastapi 의존성 주입 함수 / 각 요청마다 DB 세션 생성, 작업이 끝나면 닫는다
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session