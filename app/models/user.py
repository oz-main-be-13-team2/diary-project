# 사용자(User) 모델 정의

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)  # 사용자명
    password = Column(String(255), nullable=False)  # 암호화된 비밀번호

    # 일기(Diary)와 1:N 관계 설정
    diaries = relationship("Diary", back_populates="user", cascade="all, delete-orphan")
