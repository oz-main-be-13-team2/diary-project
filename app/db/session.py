# app/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# MySQL 연결 URL
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://diary_user:your_password@localhost:3306/diary_db"

# SQLAlchemy 엔진 생성
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,  # 연결 유지 체크
)

# 세션 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)