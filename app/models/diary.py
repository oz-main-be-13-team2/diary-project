# 일기(Diary) 모델 정의

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class Diary(Base):
    __tablename__ = "diaries"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)  # 일기 제목
    content = Column(Text, nullable=True)        # 일기 본문
    quote = Column(Text, nullable=True)          # 관련 명언
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # 생성 시각
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())  # 수정 시각
    is_deleted = Column(Boolean, server_default="0", nullable=False)  # 삭제 여부

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)  # 작성자 ID
    user = relationship("User", back_populates="diaries")  # User 모델과 관계 설정
