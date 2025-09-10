# app/models/question.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(500), nullable=False)
    # ⭐ 추가: quote_id에 ForeignKey를 설정하여 Quote 테이블과 연결합니다.
    quote_id = Column(Integer, ForeignKey("quotes.id"), nullable=False)

    # ⭐ 추가: Quote 모델의 questions와 연결되는 관계 속성을 정의합니다.
    quote_rel = relationship("Quote", back_populates="questions")