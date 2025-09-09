from app.db.base import Base
from sqlalchemy import Column, Integer, String

class Question(Base): # 질문 테이블
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String(255), nullable=False)