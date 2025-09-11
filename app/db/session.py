# 데이터베이스 연결 및 세션 관리 (PostgreSQL 비동기 버전)

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import os

# 환경변수에서 DB 접속 정보 불러오기 (없으면 기본값 사용)
DB_USER = os.getenv("DB_USER", "diary_user")
DB_PASS = os.getenv("DB_PASS", "qwer1234")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "diary_db")

# PostgreSQL + asyncpg 드라이버 사용
DATABASE_URL = "postgresql+asyncpg://diary_user:qwer1234@localhost:5432/diary_db"
# 비동기 엔진 생성
engine = create_async_engine(
    DATABASE_URL,
    echo=False,   # SQL 로그 출력 여부 (개발할 땐 True로 켜도 됨)
    future=True,
)

# 세션 팩토리 생성
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)

# FastAPI 의존성 주입용 함수
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
