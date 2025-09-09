from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base import Base  # declarative_base()로 만든 Base 불러오기

class Diary(Base):
    __tablename__ = "diaries"  # DB 테이블명

    # 기본 키 (자동 증가)
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # 일기 제목
    title = Column(String(200), nullable=False)

    # 일기 내용
    content = Column(Text, nullable=True)

    # 스크래핑한 명언 추가
    quote = Column(Text, nullable=True)  # 새로 추가

    # 작성 시간
    created_at = Column(DateTime, default=datetime.utcnow)

    # 수정 시간
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 소프트 삭제 여부
    is_deleted = Column(Boolean, default=False)

    # 작성자 ID (User 테이블과 연결)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # 관계 설정: Diary → User (N:1)
    user = relationship("User", back_populates="diaries")
