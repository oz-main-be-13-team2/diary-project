from sqlalchemy.orm import relationship

from app.db.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey


class Question(Base): # 질문 테이블
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String(255), nullable=False)

    quote_id = Column(Integer, ForeignKey("quotes.id"))
    quote = relationship("Quote", back_populates="questions")