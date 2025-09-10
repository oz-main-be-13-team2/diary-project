from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base

class Diary(Base):
    __tablename__ = "diaries"

    # PK: 기본 키, 자동 증가
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # 일기 제목 (필수)
    title = Column(String(200), nullable=False)

    # 일기 내용 (선택)
    content = Column(Text, nullable=True)

    # 스크래핑한 명언 (선택)
    quote = Column(Text, nullable=True)

    # 작성 시간 (DB 서버 시간 기준 자동 생성)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 수정 시간
    # server_default 추가 → 최초 생성 시에도 값 자동 입력
    # onupdate 추가 → 수정 시 자동 갱신
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # 소프트 삭제 여부
    # server_default="0" → DB 기본값 false 설정
    is_deleted = Column(Boolean, server_default="0", nullable=False)

    # 작성자 ID (User 테이블 FK, 유저 삭제 시 CASCADE)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # 관계 설정: Diary → User (N:1)
    # User 모델에 diaries = relationship("Diary", back_populates="user") 필요
    user = relationship("User", back_populates="diaries")
